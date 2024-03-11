from operator import is_
import random
import string
import sys
# import pyparsing for parsing

def occurs_check(v, t, dict):
    if isinstance(t, Variable):
        try:
            return occurs_check(v, dict[t.name], dict)
        except KeyError:
            return t.name == v
    for operand in t.operands:
        if occurs_check(v, operand, dict):
            return True
    return False

def add_to_dict(v,t,dict):
    if occurs_check(v,t,dict):
        return None
    dict[v] = t
    return dict

class Variable:
    def __init__(self, name="x"):
        self.name = name
    def substitute(self, dict):
        try:
            return dict[self.name]
        except KeyError:
            return self
    def free_variables(self):
        return {self.name}
    def variables(self):
        return self.free_variables()
    def rename(self, taken, new):
        try:
            return new[self.name]
        except KeyError:
            nm = self.name
            while nm in taken:
                nm += "'"
            new[self.name] = Variable(nm)
            taken.add(nm)
        return new[self.name]
    def unify(self, obj, dict):
        if isinstance(obj, Variable):
            try:
                return self.unify(dict[obj.name], dict)
            except KeyError:
                if obj.name > self.name: f,t = self.name,obj
                elif self.name > obj.name: f,t = obj.name,self
                else: return dict
                return add_to_dict(f,t,dict)
        try:
            return dict[self.name].unify(obj, dict)
        except KeyError:
            return add_to_dict(self.name, obj, dict)
    def match(self, obj):
        return {self.name : obj}
    def calculate(self, values):
        return values[self.name]
    def subterms(self):
        return [(self, lambda x: x)]
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

class Expression:
    def __init__(self, op, operands):
        self.op = op
        self.operands = operands

    def substitute(self, dict):
        new_operands = [operand.substitute(dict) for operand in self.operands]
        return Expression(self.op, new_operands)

    def variables(self):
        vars = set()
        for operand in self.operands:
            vars.update(operand.variables())
        return vars

    def free_variables(self):
        return self.variables()
    
    def subterms(self):
        def re_context(old_context,i):
            def new_context(x):
                new_operands = self.operands.copy()
                new_operands[i] = old_context(x)
                return Expression(self.op, new_operands)
            return new_context
        sts = [(self, lambda x: x)]
        for i in range(len(self.operands)):
            for (st, context) in self.operands[i].subterms():
                sts.append((st, re_context(context,i)))
        return sts

    def rename(self, taken, new):
        new_operands = []
        for operand in self.operands:
            new_operand = operand.rename(taken, new)
            new_operands.append(new_operand)
        return Expression(self.op, new_operands)

    def unify(self, obj, dict={}):
        if isinstance(obj, Expression):
            if self.op != obj.op or len(self.operands) != len(obj.operands):
                return None
            for operand1, operand2 in zip(self.operands, obj.operands):
                if operand1.unify(operand2, dict) is None:
                    return None
            return dict
        elif isinstance(obj, Variable):
            return obj.unify(self, dict)
        else:
            raise TypeError(f'{obj} is not an expression or a variable')

    def match(self, obj):
        if isinstance(obj, Expression):
            # Check if the operations and the number of operands match
            if self.op != obj.op or len(self.operands) != len(obj.operands):
                return None

            dict = {}
            for operand1, operand2 in zip(self.operands, obj.operands):
                # Recursively match the operands
                new_dict = operand1.match(operand2)
                if new_dict is None:
                    # If operands don't match, return None
                    return None

                # Check if the new substitutions conflict with existing ones
                for key, value in new_dict.items():
                    try:
                        if dict[key] is not value:
                            # If a conflict is found, return None
                            return None
                    except KeyError:
                        # If the variable is not already in the dictionary, no conflict
                        pass

                # Update the dictionary with the new substitutions
                dict.update(new_dict)

            # If all operands match and no conflicts, return the substitution dictionary
            return dict
        else:
            # If the object is not an expression, return None
            return None

    def __str__(self):
        if self.operands.__len__() > 1:
            return f"({self.op.join([str(operand) for operand in self.operands])})"
        elif self.operands.__len__() == 1:
            return f"({self.op} {self.operands[0]})"
        else:
            return self.op

    def __repr__(self):
        return str(self)

class Rule:
    def __init__(self, lhs, rhs, explanation=None, condition = None):
        self.lhs = lhs
        self.rhs = rhs
        self.explanation = explanation
        self.condition = condition

    def match(self, expr, dict={}):
        new_dict = self.lhs.match(expr)
        if new_dict is None:
            return None
        return new_dict

    def substitute(self, dict={}):
        return Rule(self.lhs.substitute(dict), self.rhs.substitute(dict)
                    , self.explanation, self.condition.substitute(dict) if self.condition is not None else None)
    
    def rename(self, taken, new):
        return Rule(self.lhs.rename(taken, new), self.rhs.rename(taken, new), self.explanation, self.condition)
    
    def variables(self):
        return self.lhs.variables()+self.rhs.variables()

    def __str__(self):
        return f"{self.lhs} = {self.rhs}"

    def __repr__(self):
        return str(self)

class Step(Rule):
    def __init__(self, rule, lhs=None, rhs=None):
        self.rule = rule
        self.explanation = rule.explanation(lhs,rhs)
        self.lhs = lhs if lhs is not None else rule.lhs
        self.rhs = rhs if rhs is not None else rule.rhs
    def rename(self, taken, new={}):
        return Step(self.rule, self.lhs.rename(taken, new), self.rhs.rename(taken, new))
    def variables(self):
        return self.lhs.variables().union(self.rhs.variables())
    def __str__(self):
        return f" = {{ {self.explanation} }}\n{self.rhs}"
    def __repr__(self):
        return f"Step({self.rule}, {self.lhs}, {self.rhs})"
    def substitute(self, dict):
        return Step(self.rule, self.lhs.substitute(dict), self.rhs.substitute(dict))

class Rewriteproof:
    def __init__(self,lhs = Variable("x"),steps=[],variables=None):
        self.lhs = lhs
        self.steps = steps
        if variables == None:
            variables = lhs.variables()
            for step in steps:
                variables.update(step.variables())
        self.variables = variables
        try:
            self.rhs = steps[-1].rhs
        except IndexError:
            self.rhs = lhs
    def substitute(self, dict):
        return Rewriteproof(self.lhs.substitute(dict), [step.substitute(dict) for step in self.steps])
    def extendByRule(self, rule):
        mp = {}
        rule = rule.rename(self.variables.copy(),mp)
        for subterm,context in self.rhs.subterms():
            unification = rule.lhs.unify(subterm,{})
            if unification is not None:
                yield Rewriteproof(self.lhs.substitute(unification),
                                  [step.substitute(unification) for step in self.steps]
                                    + [Step(rule, self.rhs.substitute(unification), context(rule.rhs).substitute(unification))])
        for subterm,context in rule.lhs.subterms():
            unification = self.rhs.unify(subterm,{})
            if unification is not None:
                yield Rewriteproof(context(self.lhs.substitute(unification)),
                                  [Step(step.rule,context(step.lhs),context(step.rhs)).substitute(unification) for step in self.steps]
                                    + [Step(rule, rule.lhs.substitute(unification), rule.rhs.substitute(unification))])
        return
    
def generate_proof(theorems, max_length=5):
    init = random.choice(theorems)
    proof = Rewriteproof(Variable())
    for _ in range(max_length):
        thm = random.choice(theorems)
        try:
            proof = random.choice(list(proof.extendByRule(thm)))
        except IndexError:
            # return a shorter proof that cannot be extended
            print(f"could not apply {thm}")
            return proof
    return proof

def stringRule(explanation,lhs,rhs):
    return Rule(lhs, rhs, (lambda lhs, rhs:explanation))
def lnot(expr):
    return Expression("\\lnot", [expr])
def wedge(expr1,expr2):
    return Expression(" \\wedge ", [expr1,expr2])
def vee(expr1,expr2):
    return Expression(" \\vee ", [expr1,expr2])

if __name__ == "__main__":
    x = Variable("x")
    y = Variable("y")
    z = Variable("z")
    # true and false:
    t = Expression("T", [])
    f = Expression("F", [])
    theorems = [
        stringRule("deMorgan", lnot(wedge(x,y)), vee(lnot(x),lnot(y))),
        stringRule("deMorgan", lnot(vee(x,y)), wedge(lnot(x),lnot(y))),
        stringRule("distributivity", wedge(x,vee(y,z)), vee(wedge(x,y),wedge(x,z))),
        stringRule("distributivity", vee(x,wedge(y,z)), wedge(vee(x,y),vee(x,z))),
        stringRule("double negation", lnot(lnot(x)), x),
        stringRule("commutativity of and", wedge(x,y),wedge(y,x)),
        stringRule("commutativity of or", vee(x,y),vee(y,x)),
        stringRule("associativity of and", wedge(x,wedge(y,z)),wedge(wedge(x,y),z)),
        stringRule("associativity of or", vee(x,vee(y,z)),vee(vee(x,y),z)),
        stringRule("identity of and", wedge(x,t),x),
        stringRule("identity of or", vee(x,f),x),
        stringRule("annihilation of and", wedge(x,f),f),
        stringRule("annihilation of or", vee(x,t),t),
        stringRule("absorption of and", wedge(x,vee(x,y)),x),
        stringRule("absorption of or", vee(x,wedge(x,y)),x),
        stringRule("idempotence of and", wedge(x,x),x),
        stringRule("idempotence of or", vee(x,x),x)
    ]
    proof = generate_proof(theorems)
    print(proof.lhs)
    for step in proof.steps:
        print(step)
