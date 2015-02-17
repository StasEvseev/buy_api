#coding: utf-8

from flask.ext.assets import Environment, Bundle

assets = Environment()

bundles = {

    'DT_JS': Bundle(
        'js/lib/jquery.dataTables.js'
    ),
    'DT_CSS': Bundle(
        'css/lib/jquery.dataTables.css',
        'css/lib/jquery.dataTables_themeroller.css',
        output='gen/css/DT.css'
    ),
    'js_all': Bundle('main.js', output='gen/packed.js'),
    'css_all': Bundle('css/main.css', output='gen/css/main.css'),

    'underscore': Bundle('js/lib/underscore-min.js'),

    'font-awesome-css': Bundle('css/lib/font-awesome-4.1.0/css/font-awesome.min.css'),

    'selectize-css': Bundle('css/lib/selectize.default.css'),

    'bootstrap-css': Bundle('css/lib/bootstrap.min.css'),
    'bootstrap-js': Bundle('js/lib/bootstrap.min.js'),

    'ng-grid-css': Bundle('css/lib/ng-grid.css'),
    'ng-grid-js': Bundle('js/lib/ng-grid.debug.js'),

    'ng-table-css': Bundle('css/lib/ng-table.min.css'),
    'ng-table-js': Bundle('js/lib/ng-table.min.js'),

    'select-js': Bundle('js/lib/select.min.js'),
    'select-css': Bundle('css/lib/select.css',
                         'css/lib/select2.css'),

    'indexmail': Bundle('js/mail/indexmail.js'),
    'prices': Bundle('js/mail/prices.js'),

    'angularjs': Bundle('js/lib/angular.js',
                        'js/lib/angular-resource.min.js',
                        'js/lib/angular-animate.min.js',
                        'js/lib/angular-route.min.js',
                        'js/lib/angular-sanitize.js',
                        'js/lib/ng-breadcrumbs.js',
                        'js/lib/angular-locale_ru-ru.js',
                        'js/angular/number.js',
                        'js/angular/auth.js',
                        'js/angular/rest.js',
                        'js/angular/table.js',
                        'js/angular/filter.js',
                        'js/angular/params.js',
                        'js/angular/modalWindow.js',
                        'js/angular/elems.js',

                        'js/bl/goodbl.js'
                        ),

    'angularjs-ui-bootstrap': Bundle('js/lib/ui-bootstrap-tpls-0.11.2.min.js'),

    'bootbox': Bundle('js/lib/bootbox.min.js'),

    # 'invoice_retail': Bundle('js/invoice.js'),



    # 'acceptance': Bundle('js/acceptance.js'),

    'metisMenu_css': Bundle('css/lib/metisMenu.css'),

    'metisMenu_js': Bundle('js/lib/metisMenu.js'),

    'custom_dash': Bundle('css/custom/sb-admin.css'),

    # 'invoicemail': Bundle('js/invoice_mail.js'),

    # 'acceptance_invoice': Bundle('js/acceptance_invoice.js'),

    # 'pointselect': Bundle('js/pointselect.js'),

    'waybilllist': Bundle('js/waybill/waybilllist.js'),

    'acceptance': Bundle('js/acceptance/acceptance.js'),

    'mail': Bundle('js/mail/mail.js'),

    'good': Bundle('js/good/good.js')
}

assets.register(bundles)