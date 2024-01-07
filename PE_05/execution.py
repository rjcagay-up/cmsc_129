def execute(order):
    stack_top = order[0]
    
    while stack_top != '$':
        print(f"k: {order}")
        if stack_top == "var":
            order.pop(0)
            order.pop(0)
            ident = list(order[0])
            identName = ident[1]
            val = execute(order)
            ident[3] = val
            order[0] = tuple(ident)
            
            order = update_tkn(order,identName,val)
            
            order.pop(0)
            order.pop(0) # remove varend
            
            if order[0] == 'IS':
                order.pop(0)
                val = execute(order)
                print(f"val: {val}")
                
                order = update_tkn(order,identName,val)
                
                order.pop(0)
            
            stack_top = order[0]
        elif stack_top == 'out':
            order.pop(0)
            order.pop(0)
            expr = execute(order)
            print(expr)
            stack_top = order[0]
        elif stack_top == 'asn':
            order.pop(0) # pops asn
            
            if order[0] == 'INTO':
                order.pop(0) # pop INTO
                ident = list(order[0])
                identName = ident[1]
                
                order.pop(0) # pop IDENT token
                order.pop(0) # pop IS
                
                expr = execute(order)
                
                order = update_tkn(order,identName,val)
                        
                order.pop(0)
                stack_top = order[0]
                
        elif stack_top == 'expr':
            order.pop(0)
            expr = execute(order)
            return expr
        elif stack_top == 'NEWLN':
            print("\n")
            order.pop(0)
            stack_top = order[0]
        elif stack_top == 'ADD':
            order.pop(0)
            expr1 = execute(order)
            order.pop(0)
            expr2 = execute(order)
            order.pop(0)
            return expr1 + expr2
        # Continue here for other num expressions
        elif stack_top[0] == 'INT_LIT':
            return int(stack_top[1]) 
        elif stack_top[0] == 'IDENT':
            return int(stack_top[3]) 
        else:
            # print(stack_top)
            order.pop(0)
            stack_top = order[0]

def update_tkn(order,identName,val):
    for i, tok in enumerate(order):
        if isinstance(tok, tuple) and tok[0] == 'IDENT' and tok[1] == identName:
            token = list(tok)
            token[3] = val
            order[i] = tuple(token)
    return order
    
    
    