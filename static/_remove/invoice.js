
var app = angular.module('myApp', ['ngResource', 'ui.bootstrap', 'ngSanitize', 'ui.select', 'AuthModule', 'NumberApp', 'RestApp',
    'Params']);

app.controller('MainCtrl', function($scope, $modal, InvoiceItems, PointSaleItems, ReceiverItems, WayBill,
                                    AcceptanceInvoiceInvoiceItem, DateWidgetScope) {

    function wrapItem(item) {
        item.count_change = function() {
            if (item.count_invoice) {
                if ($scope.model.typeInvoice == 1 && item.price_retail) {
                    item.is_approve = true;
                    item.is_can_approve = true;
                } else if ($scope.model.typeInvoice == 2 && item.price_gross) {
                    item.is_approve = true;
                    item.is_can_approve = true;
                }
            } else {
                item.is_approve = false;
                item.is_can_approve = false;
            }
        }
    }

    function wrapItems(items) {
        for (var i = 0; i < items.length; i++) {
            wrapItem(items[i]);
        }
    }

    $scope.model = {};

    $scope.model.invoice_id = INVOICE_ID;
    $scope.model.acc_id = ACCEPTANCE_ID;

    $scope.model.is_save = false;

    $scope.model.typeInvoice = 1;
    $scope.model.typeT = 1;

    $scope.model.validate = {};
    $scope.model.errors = {};

    $scope.model.date = {};

    DateWidgetScope.wrapScope($scope.model.date);

    //$scope.model.date.today = function() {
    //    $scope.model.date.dt = new Date();
    //};
    //$scope.model.date.today();
    //
    //$scope.model.date.clear = function () {
    //    $scope.model.date.dt = null;
    //};
    //
    //$scope.model.date.maxDate = '2015-06-22';
    //
    //$scope.model.date.disabled = function(date, mode) {
    //    return ( mode === 'day' && ( date.getDay() === 0 || date.getDay() === 6 ) );
    //};
    //
    //$scope.model.date.toggleMin = function() {
    //    $scope.model.date.minDate = $scope.model.date.minDate ? null : new Date();
    //};
    //$scope.model.date.toggleMin();
    //
    //$scope.model.date.open = function($event) {
    //    $event.preventDefault();
    //    $event.stopPropagation();
    //
    //    $scope.model.date.opened = true;
    //};
    //
    //$scope.model.date.dateOptions = {
    //    formatYear: 'yy',
    //    startingDay: 1
    //};
    //
    //$scope.model.date.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
    //$scope.model.date.format = $scope.model.date.formats[2];

    var loadItems = function() {
        AcceptanceInvoiceInvoiceItem.query({ acc_id: $scope.model.acc_id, id: $scope.model.invoice_id }, function(data) {
            wrapItems(data.itemss);
            $scope.calc_approve(data.items);
            $scope.model.items = data.items;
        });
    };

    $scope.openToAdd = function () {

        var modalInstance = $modal.open({
            templateUrl: '/static/template/modalAddGood.html',
            controller: 'AddToController',
            resolve: {
                items: function () {
                  return $scope.items;
                }
            }
        });

        modalInstance.result.then(function (selected) {
            console.log(selected);
            $scope.model.items.push({
                'full_name': selected.full_name,
                'price_retail': selected.price_retail,
                'price_gross': selected.price_gross,
                'good_id': selected.id,
                'count': '',
                'is_approve': true,
                'count_invoice': ''
            });
            $scope.calc_approve($scope.model.items);
            console.log("THEN1");
        }, function () {
            console.log("THEN2");
        });
    };

    loadItems();

    PointSaleItems.query({ exclude_point_id: POINTSALE_ID }, function(data) {
        $scope.model.pointsale_items = data.items;
    });

    ReceiverItems.query({ }, function(data) {
        $scope.model.receiver_items = data.items;
    });

    $scope.removeFromInvoice = function(item) {
        item.is_approve = false;
    };
    $scope.addToInvoice = function(item, typeInvoice) {
        if($scope.model.typeInvoice == 1 && !item.price_retail) {
            bootbox.alert("Ошибка!");
        } else if ($scope.model.typeInvoice == 2 && !item.price_gross) {
            bootbox.alert("Ошибка!");

        } else {
            item.is_approve = true;
        }
    };

    $scope.calc_approve = function(items) {
        for (var i = 0; i < items.length; i++) {
            var item = items[i];
            if ($scope.model.typeInvoice == 1) {
                item.is_approve = item.price_retail && item.count_invoice ? true : false;
                item.is_can_approve = item.price_retail && item.count_invoice ? true : false;
            } else {
                item.is_approve = item.price_gross && item.count_invoice ? true : false;
                item.is_can_approve = item.price_gross && item.count_invoice ? true : false;
            }
        }
    };

    $scope.checkTypeInvoice = function() {
        $scope.calc_approve($scope.model.items);
    };

    function saveRetailInvoice(force) {
        var res = $scope.model.items; //, function(elem){ return elem.is_approve; });

        var method = force?'query_confirm':'query';

        $scope.model.errors.date = $scope.model.date.dt ? false : true;
        $scope.model.errors.point_or_receiver = ($scope.model.selected_receiver && $scope.model.typeT == 2) || ($scope.model.selected_pointsale && $scope.model.typeT == 1) ? false : true;

        if($scope.model.errors.date || $scope.model.errors.point_or_receiver) {
            return;
        }

        WayBill[method]({
            'data': {
                'invoice_id': $scope.model.invoice_id,
                'items': res,
                'type': $scope.model.typeInvoice,
                'receiver_id': $scope.model.typeT == 2 ? $scope.model.selected_receiver.id : -1,
                'pointsale_id': $scope.model.typeT == 1 ? $scope.model.selected_pointsale.id : -1,
                'pointsale_from_id': POINTSALE_ID,
                'date': $scope.model.date.dt
            }
        }, function(resp) {
            var path = resp['path'];
            var status = resp['status'];

            if (status == "ok") {
                $scope.model.is_save = true;
                $scope.model.url_to_download = path;
                $scope.model.is_error = false;
                loadItems();
            } else if (status == "confirm") {
                bootbox.confirm("Внимание! Розничная накладная уже сформирована, вы хотите ее перезаписать?", function(result) {
                    if (result) {
                        saveRetailInvoice(true);
                    }
                });
            }
        }, function(resp) {
            $scope.model.message_error = resp.data['message'];
            $scope.model.is_save = false;
            $scope.model.is_error = true;
        });
    }

    $scope.saveAndPrint = function() {
        saveRetailInvoice(false);
    };
});

app.controller('AddToController', function($scope, $modalInstance, PointSaleItemItems) {

    $scope.model = {};

    $scope.model.good_items = {};

    $scope.model.selected = undefined;

    $scope.ok = function () {
        $modalInstance.close($scope.model.selected);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

    PointSaleItemItems.query({id: POINTSALE_ID}, function(data) {
        $scope.model.good_items = data.items;
    });

});

