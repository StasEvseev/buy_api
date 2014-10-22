#coding: utf-8

from flask.ext.assets import Environment, Bundle

assets = Environment()

bundles = {

    'DT_JS': Bundle(
        'js/lib/jquery.dataTables.js'
        # output='gen/js/jqueryDT.js'
    ),
    'DT_CSS': Bundle(
        'css/lib/jquery.dataTables.css',
        'css/lib/jquery.dataTables_themeroller.css',
        output='gen/css/DT.css'
    ),
    'js_all': Bundle('main.js', output='gen/packed.js'),
    'css_all': Bundle('css/main.css', output='gen/css/main.css'),

    'underscore': Bundle('js/lib/underscore-min.js'),

    'bootstrap-css': Bundle('css/lib/bootstrap.min.css'),
    'bootstrap-js': Bundle('js/lib/bootstrap.min.js'),

    'ng-grid-css': Bundle('css/lib/ng-grid.css'),
    'ng-grid-js': Bundle('js/lib/ng-grid.debug.js'),

    'select-js': Bundle('js/lib/select.min.js'),
    'select-css': Bundle('css/lib/select.css',
                         'css/lib/select2.css'),

    'prices': Bundle('js/prices.js'),

    'angularjs': Bundle('js/lib/angular.min.js',
                        #'js/lib/angular.min.js.map',
                        'js/lib/angular-resource.min.js',
                        #'js/lib/angular-resource.min.js.map',
                        'js/lib/angular-route.min.js',
                        'js/lib/angular-sanitize.js'
                        #'js/lib/angular-route.min.js.map'
                        ),

    'angularjs-ui-bootstrap': Bundle('js/lib/ui-bootstrap-tpls-0.11.2.min.js'),

    'bootbox': Bundle('js/lib/bootbox.min.js'),

    'invoice_retail': Bundle('js/invoice_retail.js')

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