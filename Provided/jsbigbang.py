import ply.lex as lex
import ply.yacc as yacc
import graphics as graphics
import jstokens
import jsgrammar
import jsinterp 
import htmltokens
import htmlgrammar

# Load up the lexers and parsers that you have already written in
# previous assignments. Do not worry about the "module" or 
# "tabmodule" arguments -- they handle storing the JavaScript
# and HTML rules separately. 
htmllexer  = lex.lex(module=htmltokens) 
htmlparser = yacc.yacc(module=htmlgrammar,tabmodule="parsetabhtml") 
jslexer    = lex.lex(module=jstokens) 
jsparser   = yacc.yacc(module=jsgrammar,tabmodule="parsetabjs") 

# The heart of our browser: recursively interpret an HTML abstract
# syntax tree. 
def interpret(ast):     
    print "Entering interpret, ast = " + str(ast)
    for node in ast:
        nodetype = node[0]
        if nodetype == "word-element":
            #graphics.word(node[1]) 
            print '\nWord Elements:\n' + node[1]
        elif nodetype == "tag-element":
            tagname = node[1];
            tagargs = node[2];
            subast = node[3];
            closetagname = node[4]; 
            if (tagname <> closetagname):
                #graphics.warning("(mistmatched " + tagname + " " + closetagname + ")")
                print "\nError:\n(mistmatched " + tagname + " " + closetagname + ")"
            else: 
                #graphics.begintag(tagname,tagargs);
                interpret(subast)
                #graphics.endtag(); 
        elif nodetype == "javascript-element": 
            jstext = node[1]; 
            jsast = jsparser.parse(jstext,lexer=jslexer) 
            result = jsinterp.interpret(jsast)
            # Now interpret result in case it contains HTML tags
            jshtmlast = htmlparser.parse(result,lexer=htmllexer)
            interpret(jshtmlast)
            #print '\nJS Result:\n' + str(jshtmlast)
            #graphics.word(result) 

# Here is an example webpage that includes JavaScript that generates HTML.
# You can use it for testing.
webpage = """<html>
<h1>JavaScript That Produces HTML</h1>
<p>
This paragraph starts in HTML ...
<script type="text/javascript">
write("<b>This whole sentence should be bold, and the concepts in this problem touch on the <a href='http://en.wikipedia.org/wiki/Document_Object_Model'>Document Object Model</a>, which allows web browsers and scripts to <i>manipulate</i> webpages.</b>");
</script> 
... and this paragraph finishes in HTML. 
</p> 
<hr> </hr> <!-- draw a horizontal bar --> 
<p> 
Now we will use JavaScript to display even numbers in <i>italics</i> and
odd numbers in <b>bold</b>. <br> </br> 
<script type="text/javascript">
function tricky(i) {
  if (i <= 0) {
    return i; 
  } ; 
  if ((i % 2) == 1) {
    write("<b>");
    write(i); 
    write("</b>"); 
  } else {
    write("<i>");
    write(i); 
    write("</i>"); 
  }
  return tricky(i - 1); 
} 
tricky(10);
</script> 
</p> 
</html>"""

htmlast = htmlparser.parse(webpage,lexer=htmllexer) 
#graphics.initialize() # let's start rendering a webpage
interpret(htmlast) 
#graphics.finalize() # we're done rendering this webpage

