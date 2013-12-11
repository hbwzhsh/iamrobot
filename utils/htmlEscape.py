# coding=utf-8
__author__ = 'zhuwei'

import optparse
import sys
import os
from xml.sax.saxutils import escape, unescape

html_escape_dict = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
    '¢': '&cent;',
    '©': '&copy;',
    '÷': '&divide;',
    '®': '&reg;',
    '¦': '&brvbar;',
    '¨': '&uml;',
    'µ': '&micro;',
    '·': '&middot;',
    '¶': '&para;',
    '±': '&plusmn;',
    '€': '&euro;',
    '£': '&pound;',
    '§': '&sect;',
    '™': '&trade;',
    '¥': '&yen;',
    'á': '&aacute;',
    'Á': '&Aacute;',
    'à': '&agrave;',
    'À': '&Agrave;',
    'â': '&acirc;',
    'Â': '&Acirc;',
    'å': '&aring;',
    'Å': '&Aring;',
    'ã': '&atilde;',
    'Ã': '&Atilde;',
    'ä': '&auml;',
    'Ä': '&Auml;',
    'æ': '&aelig;',
    'Æ': '&AElig;',
    'ç': '&ccedil;',
    'Ç': '&Ccedil;',
    'é': '&eacute;',
    'É': '&Eacute;',
    'è': '&egrave;',
    'È': '&Egrave;',
    'ê': '&ecirc;',
    'Ê': '&Ecirc;',
    'ë': '&euml;',
    'Ë': '&Euml;',
    'í': '&iacute;',
    'Í': '&Iacute;',
    'ì': '&igrave;',
    'Ì': '&Igrave;',
    'î': '&icirc;',
    'Î': '&Icirc;',
    'ï': '&iuml;',
    'Ï': '&Iuml;',
    'ñ': '&ntilde;',
    'Ñ': '&Ntilde;',
    'ó': '&oacute;',
    'Ó': '&Oacute;',
    'ò': '&ograve;',
    'Ò': '&Ograve;',
    'ô': '&ocirc;',
    'Ô': '&Ocirc;',
    'ø': '&oslash;',
    'Ø': '&Oslash;',
    'õ': '&otilde;',
    'Õ': '&Otilde;',
    'ö': '&ouml;',
    'Ö': '&Ouml;',
    'ß': '&szlig;',
    'ú': '&uacute;',
    'Ú': '&Uacute;',
    'ù': '&ugrave;',
    'Ù': '&Ugrave;',
    'û': '&ucirc;',
    'Û': '&Ucirc;',
    'ü': '&uuml;',
    'Ü': '&Uuml;',
    'ÿ': '&yuml;',
    '–': '&ndash;',
    '—': '&mdash;',
    '¡': '&iexcl;',
    '¿': '&iquest;',
    '“': '&ldquo;',
    '”': '&rdquo;',
    '‘': '&lsquo;',
    '’': '&rsquo;',
    '«': '&laquo;',
    '»': '&raquo;',
    ' ': '&nbsp;',
    '�': '&shy;',
    '¹': '&sup1',
    'º': '&ordm;',
    '¼': '&frac14;',
    '½': '&frac12;',
    '¾': '&frac34;',
    '×': '&times;',
    '¬': '&not;',
    'ª': '&ordf;',
    '²': '&sup2;',
    '³': '&sup3;',
    '´': '&acute;',
    '∀': '&forall;',
    '∂': '&part;',
    '∃': '&exist;',
    '∅': '&empty;',
    '∇': '&nabla;',
    '∈': '&isin;',
    '∉': '&notin;',
    '∋': '&ni;',
    '∏': '&prod;',
    '∑': '&sum;',
    '−': '&minus;',
    '∗': '&lowast;',
    '√': '&radic;',
    '∝': '&prop;',
    '∞': '&infin;',
    '∠': '&ang;',
    '∧': '&and;',
    '∨': '&or;',
    '∩': '&cap;',
    '∪': '&cup;',
    '∫': '&int;',
    '∴': '&there4;',
    '∼': '&sim;',
    '≅': '&cong;',
    '≈': '&asymp;',
    '≠': '&ne;',
    '≡': '&equiv;',
    '≤': '&le;',
    '≥': '&ge;',
    '⊂': '&sub;',
    '⊃': '&sup;',
    '⊄': '&nsub;',
    '⊆': '&sube;',
    '⊇': '&supe;',
    '⊕': '&oplus;',
    '⊗': '&otimes;',
    '⊥': '&perp;',
    '⋅': '&sdot;',
    'α': '&alpha;',
    'β': '&beta;',
    'γ': '&gamma;',
    'Α': '&Alpha;',
    'Β': '&Beta;',
    'Γ': '&Gamma;',
    'Δ': '&Delta;',
    'Ε': '&Epsilon;',
    'Ζ': '&Zeta;',
    'Η': '&Eta;',
    'Θ': '&Theta;',
    'Ι': '&Iota;',
    'Κ': '&Kappa;',
    'Λ': '&Lambda;',
    'Μ': '&Mu;',
    'Ν': '&Nu;',
    'Ξ': '&Xi;',
    'Ο': '&Omicron;',
    'Π': '&Pi;',
    'Ρ': '&Rho;',
    'Σ': '&Sigma;',
    'Τ': '&Tau;',
    'Υ': '&Upsilon;',
    'Φ': '&Phi;',
    'Χ': '&Chi;',
    'Ψ': '&Psi;',
    'Ω': '&Omega;',
    'δ': '&delta;',
    'ε': '&epsilon;',
    'ζ': '&zeta;',
    'η': '&eta;',
    'θ': '&theta;',
    'ι': '&iota;',
    'κ': '&kappa;',
    'λ': '&lambda;',
    'ν': '&nu;',
    'ϑ': '&thetasym;',
    'ϒ': '&upsih;',
    'ϖ': '&piv;',
    '↑': '&uarr;',
    '→': '&rarr;',
    '←': '&larr;',
    '↓': '&darr;',
    '↔': '&harr;',
    '↵': '&crarr;',
    '⌈': '&lceil;',
    '⌉': '&rceil;',
    '⌊': '&lfloor;',
    '⌋': '&rfloor;',
    '◊': '&loz;',
    '♠': '&spades;',
    '♣': '&clubs;',
    '♥': '&hearts;',
    '♦': '&diams;',
    '…': '&hellip;',
    '‰': '&permil;',
    'Œ': '&OElig;',
    'œ': '&oelig;',
    'Š': '&Scaron;',
    'š': '&scaron;',
    'Ÿ': '&Yuml;',
    'ƒ': '&fnof;',
    'ˆ': '&circ;',
    '˜': '&tilde;'
}

html_unescaped_dict = {}
for k, v in html_escape_dict.items():
    html_unescaped_dict[v] = k


def read_file_by_buffer(filename, buffer_size=50000):
    buffer_size = buffer_size
    f = file(filename, 'r')
    string_buffer = f.read(buffer_size)
    total_size = os.path.getsize(filename)
    file_string = ""
    while len(string_buffer):
        file_string += buffer
        f_progress = 100.0 * len(file_string) / total_size
        os.write(1, "\r Progress[%.3f %% (%d/%d)]" % (f_progress, len(file_string), total_size))
        sys.stdout.flush()
        string_buffer = f.read(buffer_size)
    f.close()
    print "\n Read f %s Finished" % filename
    return file_string


def save_result_file(string, output_dir):
    with open(output_dir, 'a+') as result_file:
        result_file.write(string)


"""
&amp=>&
"""

def escape_html(input_file, output_file=os.getcwd() + '/'):
    f = file(input_file, 'r')
    for line in f.xreadlines():
        if output_file == os.getcwd() + '/':
            save_result_file(escape(line, html_escape_dict), output_file + input_file + '_escape')
        else:
            save_result_file(escape(line, html_escape_dict), output_file + '_escape')

"""
&=>&amp;
"""

def unescape_html(input_file, output_file=os.getcwd() + '/'):
    f = file(input_file, 'r')
    for line in f.xreadlines():
        if output_file == os.getcwd() + '/':
            save_result_file(unescape(line, html_unescaped_dict), output_file + input_file + '_escape')
        else:
            save_result_file(unescape(line, html_unescaped_dict), output_file + '_escape')


def main():
    usage = """
    htmlEscape.py -i <INPUT File> -m <Escape or Unescape> \n
    Example: python htmlEscape.py -i demo.txt -m e[, -o output_file_name]
    """
    fmt = optparse.IndentedHelpFormatter(max_help_position=50,
                                         width=100)
    parser = optparse.OptionParser(usage=usage, formatter=fmt)
    parser.add_option('-i', '--input',
                      help='Input File')
    parser.add_option('-o', '--output',
                      help='Output Dir')
    parser.add_option('-m', '--mod',
                      help='Choose Escape(&=>&amp;) Please type -m e or \n\r Unescape(&amp;=>&) please type -m u')
    options, args = parser.parse_args()
    if not options.input:
        print 'Hrrrm....You’re looking swell, Dolly\n but i need a input filename'
        sys.exit(1)
    elif not options.mod:
        print u'请选择要执行 &amp;=>& 这类操作还是 &=>&amp; 具体帮助请使用 "-h" 参数'
        sys.exit(1)
    elif not options.output:
        if options.mod == 'e':
            escape_html(options.input)
        elif options.mod == 'u':
            unescape_html(options.input)
        else:
            print 'Error! Wrong Args, For more please type python htmlEscape.py -h'
            sys.exit(1)
    elif options.output:
        if options.mod == 'e':
            escape_html(options.input, options.output)
        elif options.mod == 'u':
            unescape_html(options.input, options.output)
        else:
            print 'Error! Wrong Args, For more please type python htmlEscape.py -h'
            sys.exit(1)
    else:
        print "Hrrm....You're looking ...Hrrrm...,Bad args!"
        sys.exit(1)


if __name__ == "__main__":
    main()