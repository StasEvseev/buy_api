#coding: utf-8

from flask.ext.assets import Environment, Bundle

assets = Environment()

bundles = {

    'DT_JS': Bundle(
        'js/lib/jquery.dataTables.js',
        output='gen/js/jqueryDT.js'
    ),
    'DT_CSS': Bundle(
        'css/lib/jquery.dataTables.css',
        'css/lib/jquery.dataTables_themeroller.css',
        output='gen/css/DT.css'
    ),
    'js_all': Bundle('main.js', output='gen/packed.js'),
    'css_all': Bundle('css/main.css', output='gen/css/main.css')

    # 'home_js': Bundle(
    #     'js/lib/jquery-1.10.2.js',
    #     'js/home.js',
    #     output='gen/home.js'),
    #
    # 'home_css': Bundle(
    #     'css/lib/reset.css',
    #     'css/common.css',
    #     'css/home.css',
    #     output='gen/home.css'),
    #
    # 'admin_js': Bundle(
    #     'js/lib/jquery-1.10.2.js',
    #     'js/lib/Chart.js',
    #     'js/admin.js',
    #     output='gen/admin.js'),
    #
    # 'admin_css': Bundle(
    #     'css/lib/reset.css',
    #     'css/common.css',
    #     'css/admin.css',
    #     output='gen/admin.css')
}

assets.register(bundles)

# js = Bundle('main.js', output='gen/packed.js')
# assets.register('js_all', js)