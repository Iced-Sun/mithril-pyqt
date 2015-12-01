run([
    ('Basic label', label('Hello world!')),
    ('Basic label2', label('Hello world!'))),
    ('Label with attr', m('label', '<b>Bold and indent</b>', {'indent': 20})),
    ('Nested label', m('label', 'outer', m('label', 'inner'))),
])
