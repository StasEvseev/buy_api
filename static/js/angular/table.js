angular.module('TableHelper', [])


.factory("TableWrapScope", function(ngTableParams) {

        return {
            wrapScope: function (scope, resource, sorting) {
                var loadData = function(func_success, defer) {

                    var filter_field = scope.filter_field;
                    var filter_text = scope.filter_text;
                    var sort_field = scope.sort_field;
                    var sort_course = scope.sort_course;
                    var page = scope.page;
                    var count = scope.count;

                    var attrIfDef = function(attr_name, attr, obj) {
                        if(attr) {
                            obj[attr_name] = attr;
                        }
                    };

                    var params = {};

                    attrIfDef('filter_field', filter_field, params);
                    attrIfDef('filter_text', filter_text, params);
                    attrIfDef('sort_field', sort_field, params);
                    attrIfDef('sort_course', sort_course, params);
                    attrIfDef('page', page, params);
                    attrIfDef('count', count, params);

                    resource.query(params, function(data) {
                        if (func_success) {
                            func_success(data);
                        }
                        defer.resolve(data.items);
                    });
                };

                scope.tableParams = new ngTableParams({
                    page: 1,            // show first page
                    count: 10,
                    sorting: sorting
                }, {
                    total: 0,           // length of data
                    getData: function($defer, params) {

                        scope.count = params.count();

                        scope.page = params.page();
                        var filter = params.filter();
                        var sort = params.sorting();

                        scope.filter_field = _.keys(filter)[0];
                        scope.filter_text = filter[scope.filter_field];
                        scope.sort_field = _.keys(sort)[0];
                        scope.sort_course = sort[scope.sort_field];

                        loadData(function(data) {
                            params.total(data.max);
                        }, $defer);
                    }
                });
            }
        };
})


.factory("load", function() {
    return {
        loadData: function (func, restapi_func, params, scope) {

            var filter_field = scope.model.filter_field;
            var filter_text = scope.model.filter_text;
            var sort_field = scope.model.sort_field;
            var sort_course = scope.model.sort_course;
            var page = scope.model.page;
            var count = scope.model.count;

            var attrIfDef = function (attr_name, attr, obj) {
                if (attr) {
                    obj[attr_name] = attr;
                }
            };

            attrIfDef('filter_field', filter_field, params);
            attrIfDef('filter_text', filter_text, params);
            attrIfDef('sort_field', sort_field, params);
            attrIfDef('sort_course', sort_course, params);
            attrIfDef('page', page, params);
            attrIfDef('count', count, params);

            restapi_func(params, func);
        }
    }
})
    .factory('wrapItemsToChangeCount', function() {
        function wrapItem(item, typeInv) {
            item.count_change = function(typeInvoice) {
                if (_.isNumber(parseInt(item.count_invoice)) && parseInt(item.count_invoice) > 0) {
                    if (typeInvoice == 1 && item.price_retail) {
                        item.is_approve = true;
                        item.is_can_approve = true;
                    } else if (typeInvoice == 2 && item.price_gross) {
                        item.is_approve = true;
                        item.is_can_approve = true;
                    }
                } else {
                    item.is_approve = true;
                }
            };

            if (typeInv == 1) {
                item.is_approve = item.price_retail  ? true : false;
                item.is_can_approve = item.price_retail ? true : false;
            } else if (typeInv == 2) {
                item.is_approve = item.price_gross  ? true : false;
                item.is_can_approve = item.price_gross ? true : false;
            } else {
                item.is_approve = item.price  ? true : false;
                item.is_can_approve = item.price ? true : false;
            }
//            item.is_approve = true;
        }

        return {
            wrapItem: wrapItem,
            wrapItems: function(items, typeInvoice) {
                for (var i = 0; i < items.length; i++) {
                    wrapItem(items[i], typeInvoice);
                }
            }
        }
    })
    .factory('InvoiceItemHelper', function() {
        return {
            removeFromInvoice: function (item) {
                item.is_approve = false;
            },
            addToInvoice: function (item, typeInvoice) {
                if (typeInvoice == 1 && !item.price_retail) {
                    bootbox.alert("Ошибка!");
                } else if (typeInvoice == 2 && !item.price_gross) {
                    bootbox.alert("Ошибка!");
                } else {
                    item.is_approve = true;
                }
            }
        }

    });