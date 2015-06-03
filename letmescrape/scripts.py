
def make_lua_script(selector):
    script = """
            function main(splash)
                splash:go(splash.args.url)
                while(splash:evaljs("document.querySelector('"""+selector+"""') == null"))
                do
                    splash:wait(0.05)
                end
                return splash:html()
            end
            """
    return script