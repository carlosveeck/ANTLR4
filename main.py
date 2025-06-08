from antlr4 import *
from ArithmeticLexer import ArithmeticLexer
from ArithmeticParser import ArithmeticParser

class ArithmeticVisitor:
    def __init__(self):
        self.memory = {}

    def visit(self, ctx):
        if ctx is None:
            return None

        ctx_type = type(ctx).__name__

        if ctx_type == 'ProgramContext':
            return self.visitProgram(ctx)
        elif ctx_type == 'StatementContext':
            return self.visitStatement(ctx)
        elif ctx_type == 'AssignmentContext':
            return self.visitAssignment(ctx)
        elif ctx_type == 'ExprContext':
            return self.visitExpr(ctx)
        elif ctx_type == 'TermContext':
            return self.visitTerm(ctx)
        elif ctx_type == 'FactorContext':
            return self.visitFactor(ctx)

        raise Exception(f"Visitação não implementada para {ctx_type}")

    def visitProgram(self, ctx):
        result = None
        for st in ctx.statement():
            result = self.visit(st)
        return result

    def visitStatement(self, ctx):
        if ctx.assignment():
            return self.visitAssignment(ctx.assignment())
        else:
            return self.visitExpr(ctx.expr())

    def visitAssignment(self, ctx):
        var_name = ctx.VAR().getText()
        value = self.visitExpr(ctx.expr())
        self.memory[var_name] = value
        return value

    def visitExpr(self, ctx):
        result = self.visitTerm(ctx.term(0))
        for i in range(1, len(ctx.term())):
            op = ctx.getChild(i * 2 - 1).getText()
            if op == '+':
                result += self.visitTerm(ctx.term(i))
            else:
                result -= self.visitTerm(ctx.term(i))
        return result

    def visitTerm(self, ctx):
        result = self.visitFactor(ctx.factor(0))
        for i in range(1, len(ctx.factor())):
            op = ctx.getChild(i * 2 - 1).getText()
            if op == '*':
                result *= self.visitFactor(ctx.factor(i))
            else:
                result /= self.visitFactor(ctx.factor(i))
        return result

    def visitFactor(self, ctx):
        if ctx.INT():
            return int(ctx.INT().getText())
        elif ctx.VAR():
            var_name = ctx.VAR().getText()
            if var_name in self.memory:
                return self.memory[var_name]
            else:
                raise Exception(f"Variável '{var_name}' não definida")
        elif ctx.expr():
            return self.visitExpr(ctx.expr())
        else:
            raise Exception("Erro: nó factor inesperado")


def main():
    visitor = ArithmeticVisitor()
    print("REPL Aritmético. Digite expressões ou atribuições. Ctrl+C para sair.")

    try:
        while True:
            text = input(">>> ")
            if not text.strip():
                continue

            lexer = ArithmeticLexer(InputStream(text))
            stream = CommonTokenStream(lexer)
            parser = ArithmeticParser(stream)
            tree = parser.statement()
            result = visitor.visit(tree)
            if result is not None:
                print(result)

    except KeyboardInterrupt:
        print("\nSaindo...")

    except Exception as e:
        print("Erro:", e)


if __name__ == '__main__':
    main()
