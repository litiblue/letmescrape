
def make_lua_script(selectors, bitwise_operators=""):

    lua_string = """"""
    for index, selector in enumerate(selectors):

        if index == 0:
            lua_string = lua_string + 'document.querySelector("' + selector + '") == null '
        else:
            lua_string = lua_string + bitwise_operators + ' document.querySelector("' + selector + '") == null '

    script = """
            function main(splash)
                splash:go(splash.args.url)
                while(splash:evaljs('"""+lua_string+"""'))
                do
                    splash:wait(0.05)
                end
                return splash:html()
            end
            """
    return script

