"""Regression coverage for the two failures found in published math."""
import html
import unittest
from build_blog import normalize_latex, math_markup, render_math


class BlogMathTests(unittest.TestCase):
    def test_macro_prefixes_are_not_commands(self):
        self.assertEqual(normalize_latex(r'\Delta t + \delta x + \Gamma + \epsilon'),
                         r'\Delta t + \delta x + \Gamma + \epsilon')
        self.assertEqual(normalize_latex(r'\D x + \E + \dd t'),
                         r'\mathcal{D} x + \mathcal{E} + \mathop{}\!\mathrm{d} t')

    def test_nested_average_and_bold_greek(self):
        self.assertEqual(normalize_latex(r'\avg{\frac{\bm\phi}{2}}'),
                         r'\left\langle \frac{\boldsymbol\phi}{2}\right\rangle')

    def test_aligned_tex_and_html_characters_survive(self):
        source = r'\begin{aligned}\Delta x&=a\\x&<b\end{aligned}'
        result = math_markup(source, 'block')
        self.assertIn('&amp;', result)
        self.assertIn('&lt;', result)
        self.assertEqual(html.unescape(result),
                         '<div class="arithmatex">\\[' + source + '\\]</div>')

    def test_only_math_is_normalized(self):
        source = '<code>\\D</code><span class="arithmatex">\\(\\Delta t\\)</span>'
        self.assertEqual(render_math(source), source)


if __name__ == '__main__':
    unittest.main()
