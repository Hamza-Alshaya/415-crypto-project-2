#TO BE IMPLEMENTED: helper functions that simplify print formatting using escape sequences

#tf = text_format
class tf:
    NORMAL              ="\033[0;"
    BOLD                ="\033[1;"
    ITALIC              ="\033[3;"
    UNDERLINE           ="\033[4;"
    BLINK               ="\033[5;"
    INVERSE             ="\033[7;"
    RESET               ="\033[0m"

    RED                 ="31"
    GREEN               ="32"
    YELLOW              ="33"
    BLUE                ="34"
    MAGENTA             ="35"
    CYAN                ="36"
    WHITE               ="37"
    GRAY                ="90"
    GREY                ="90"
    BRIGHTRED           ="91"
    BRIGHTGREEN         ="92"
    BRIGHTYELLOW        ="93"
    BRIGHTBLUE          ="94"
    BRIGHTMAGENTA       ="95"
    BRIGHTCYAN          ="96"
    BRIGHTWHITE         ="97"

    NOBG                ="m"
    REDBG               =";41m"
    GREENBG             =";42m"
    YELLOWBG            =";43m"
    BLUEBG              =";44m"
    MAGENTABG           =";45m"
    CYANBG              =";46m"
    WHITEBG             =";47m"
    GRAYBG              =";100m"
    GREYBG              =";100m"
    BRIGHTREDBG         =";101m"
    BRIGHTGREENBG       =";102m"
    BRIGHTYELLOWBG      =";103m"
    BRIGHTBLUEBG        =";104m"
    BRIGHTMAGENTABG     =";105m"
    BRIGHTCYANBG        =";106m"
    BRIGHTWHITEBG       =";107m"

class tf_presets:
    warning = f'{tf.BOLD}{tf.WHITE}{tf.YELLOWBG}'
    success = f'{tf.BOLD}{tf.WHITE}{tf.GREENBG}'
    info = f'{tf.BOLD}{tf.WHITE}{tf.BLUEBG}'
    danger = f'{tf.BOLD}{tf.WHITE}{tf.REDBG}'
    danger_blink = f'{tf.BLINK}{tf.WHITE}{tf.REDBG}'
    green = f'{tf.NORMAL}{tf.GREEN}{tf.NOBG}'
    red = f'{tf.NORMAL}{tf.RED}{tf.NOBG}'
    purple = f'{tf.NORMAL}{tf.MAGENTA}{tf.NOBG}'
    blue = f'{tf.NORMAL}{tf.CYAN}{tf.NOBG}'
            
    def colorize(string, preset):
        return f'{preset}{string}{tf.RESET}'