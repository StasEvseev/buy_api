angular.module("ModalApp", ["NumberApp", "FilterApp", "ngAnimate"])

.controller('AddToController', function($scope, $modalInstance, PointSaleItemItems, pointsale_from_id, good_exclude) {

    $scope.model = {};

    $scope.pointsale_from_id = pointsale_from_id;
    $scope.good_exclude = good_exclude;

    console.log($scope.good_exclude);

    $scope.model.good_items = {};

    $scope.model.selected = undefined;

    $scope.ok = function () {
        $modalInstance.close($scope.model.selected);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

    PointSaleItemItems.query({
        id: $scope.pointsale_from_id, exclude_items: {array: $scope.good_exclude}
    }, function(data) {
        $scope.model.good_items = data.items;
    });

})

/*
 * Контроллер для модального окна создания продукта с ценой(указывается цена с НДС, без НДС, процент НДС, оптовая
 * и розничная цены.
* */
.controller('AddGoodCtrl', function($scope, $modal, $modalInstance, object) {

        $scope.model = {};

        $scope.object = object;

        console.log("WINDOW", object);

//        if (object) {
//            $scope.object = object;
////            $scope.model.good.id = object.good_id;
////            $scope.model.NDS = object.NDS;
////            $scope.model.price_pre = object.price_pre;
////            $scope.model.price_post = object.price_post;
////            $scope.model.price_retail = object.price_retail;
////            $scope.model.price_gross = object.price_gross;
//        }

        $scope.model.disS = true;

        $scope.func_fill_form = function () {
            $scope.model.disS = false;
        };

        $scope.func_unfill_form = function() {
            $scope.model.disS = true;
        };

        $scope.ok = function () {
            var record = $scope.func_save_form();
            if (record) {
                $modalInstance.close(record);
            }
        };

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
})

.controller('PointSaleCtrl',
    function($scope, object, PointSaleItem, PointSaleItems, $modalInstance) {
        var isNew = true;
        $scope.model = {};
        if (object) {
            isNew = false;
            $scope.model.name = object.name;
            $scope.model.address = object.address;
        }

        $scope.ok = function() {
            if(isNew) {
                PointSaleItems.save({
                    data: {
                        name: $scope.model.name,
                        address: $scope.model.address
                    }
                }, function (data) {
                    $modalInstance.close(data);
                }, function(data) {

                })
            } else {

            }
        };

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    }
)

/*
* Контроллер для создание новых продуктов (номенклатура с номерами - глобальным и локальным).
* */
.controller('AddNewGoodCtrl', function($scope, $modal, $modalInstance, object, CommodityItems, CommodityId, GoodItems, GoodItem) {
        var good = object;
        var isNumericCalc = function(numeric) {
            $scope.isCollapsedNumber = numeric ? false: true;
            isNumeric = numeric;
        };
        var isNumeric = false;
        var isNew = true;

        $scope.model = {};

        if(good) {
            isNew = false;
            CommodityId.query({id:good.commodity_id}, function (data) {
                $scope.model.commodity_selected = data;
                isNumericCalc(data.numeric);
                $scope.model.number_local = good.number_local;
                $scope.model.number_global = good.number_global;
            });
        }

        $scope.model.commodity_items = {};

        $scope.model.validate = {};
        $scope.model.success = {};
        $scope.model.errors = {};
        $scope.model.errors.number_local = false;
        $scope.model.errors.number_global = false;

        $scope.model.selected = undefined;

        $scope.commoditySelect = function (item, model) {

            isNumericCalc(item.numeric);

            $scope.model.number_global = undefined;
            $scope.model.number_local = undefined;

            $scope.isCollapsedPrice = false;

        };

        $scope.isCollapsedNumber = true;
        $scope.isCollapsedPrice = true;
        $scope.isCollapsed = true;

        var setError = function(attr, message) {
            if (message) {
                $scope.model.validate[attr] = message;
                $scope.model.errors[attr] = true;
            } else {
                $scope.model.validate[attr] = "";
                $scope.model.errors[attr] = false;
            }
        };

        var setSuccess = function(attr, value) {
            $scope.model.success[attr] = value;
        };

        $scope.ok = function () {

            if (isNumeric) {
                if(!$scope.model.number_local) {
                    setError("number_local", "Заполните поле номер в пределах года.");
                } else {
                    setError("number_local");
                }
                if(!$scope.model.number_global) {
                    setError("number_global", "Заполните поле номер(общую).");
                } else {
                    setError("number_global");
                }
            }

            if (_.indexOf(_.values($scope.model.errors), true) != -1) {
                return;
            }

            if (isNew) {
                GoodItems.save({
                    data: {
                        commodity_id: $scope.model.commodity_selected.id,
                        number_local: $scope.model.number_local,
                        number_global: $scope.model.number_global
                    }
                }, function(data) {
                    $modalInstance.close(data);
                }, function (data) {
                    $scope.model.validate.message = data.data.message;
                });
            } else {
                GoodItem.update({id: good.id, data: {
                    commodity_id: $scope.model.commodity_selected.id,
                    number_local: $scope.model.number_local,
                    number_global: $scope.model.number_global
                }}, function(data) {
                    $modalInstance.close(data);
                });
            }
        };

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
//
//        $scope.loadCommodity = function(commodity) {
//
//            CommodityItems.query({}, function(data) {
//                $scope.model.commodity_items = data.items;
//                if (commodity) {
//                    $scope.model.commodity_selected = commodity;
//                    $scope.commoditySelect(commodity);
//                }
//            });
//        };

        $scope.resource = CommodityItems.query;

//        $scope.loadCommodity();

})

/*
* Контроллер для создания новой номеклатуры с указанием безномерной или номерной.
* */
.controller('ComCtrl', function($scope, $modalInstance, object, CommodityItems, CommodityId) {

        var isNew = true;
        $scope.model = {};
        $scope.model.numeric = true;
        $scope.model.errors = {};
        $scope.model.validate = {};

        console.log(object);

        if(object) {
            isNew = false;
            $scope.model.thematic = object.thematic;
            $scope.model.numeric = object.numeric;
            $scope.model.name = object.name;
        }

        var setError = function(attr, message) {
            if (message) {
                //$scope.model.validate[attr] = message;
                $scope.model.errors[attr] = true;
            } else {
                //$scope.model.validate[attr] = "";
                $scope.model.errors[attr] = false;
            }
        };

        $scope.ok = function () {
            if(!$scope.model.name) {
                setError("name", "Поле наименование не должно быть пустым");
                $scope.model.validate.message = "Поле наименование не должно быть пустым";
            } else {
                setError("name");
                $scope.model.validate.message = undefined;
            }
            if (_.indexOf(_.values($scope.model.errors), true) != -1) {
                return;
            }

            if(isNew) {
                CommodityItems.save({data: {
                    'name': $scope.model.name,
                    'thematic': $scope.model.thematic ? $scope.model.thematic : '',
                    'numeric': $scope.model.numeric}},
                    function(data) {
                        $modalInstance.close(data);
                    },
                    function(data) {
                        console.log(data);
                        setError("name", "Поле наименование должны быть уникальным");
                        $scope.model.validate.message = data.data.message;
                    }
                );
            } else {
                CommodityId.update({id: object.id, data: {
                        name: $scope.model.name,
                        thematic: $scope.model.thematic ? $scope.model.thematic : '',
                        numeric: $scope.model.numeric
                    }},
                    function(data) {
                        $modalInstance.close(data);
                    }, function (data) {

                    })
            }
        };

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
});