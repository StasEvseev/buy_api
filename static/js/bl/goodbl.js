angular.module('GoodModule', ['ElemsModule'])
.directive('goodForm', function(GoodItems, PriceHelper, $modal) {
    return {
        restrict: 'E',
        scope: {
            'fillclbk': '=',
            'unfillclbk': '=',
            'saveclbk': '=',
            model: "="
        },
        templateUrl: '/static/template/goodbl/good-form.html',
        controller: function($scope) {

            var RATE_RETAIL = 1.6;
            var RATE_GROSS = 1.4;

            /*
            * Подгрузка предполагаемой цены из системы.
            * */
            $scope.getPrice = function() {
                PriceHelper.get({
                    'good_id': $scope.model.good_selected.id,
                    'price_post': $scope.model.price_post
                }, function(data) {
                    $scope.model.price_recommendation = data.items;
                    $scope.isCollapsed = false;
                });
            };

            $scope.priceChange = function() {
                $scope.model.price_retail_rec = $scope.model.price_post * RATE_RETAIL;
                $scope.model.price_gross_rec = $scope.model.price_post * RATE_GROSS;
            };

            $scope.compare_info = function(value, value1) {
                return parseFloat(value).toFixed(2) === parseFloat(value1).toFixed(2);
            };

            $scope.compare_warning = function(value, value1) {
                return parseFloat(value).toFixed(2) < parseFloat(value1).toFixed(2);
            };

            $scope.compare_success = function(value, value1) {
                return parseFloat(value).toFixed(2) > parseFloat(value1).toFixed(2);
            };

            $scope.setRec = function(price_retail, price_gross) {
                if(!_.isUndefined(price_retail)) {
                    $scope.model.price_retail = price_retail;
                }
                if(!_.isUndefined(price_gross)) {
                    $scope.model.price_gross = price_gross;
                }
            };

            $scope.saveclbk = function() {
                if (!$scope.model.good_selected) {
                    $scope.model.errors.good = true;
                    $scope.model.validate.message = "Не выбран товар";
                    return;
                } else if (!$scope.model.price_post) {
                    $scope.model.errors.price_post = true;
                    $scope.model.errors.good = false;
                    $scope.model.validate.message = "Не указана цена за товар с НДС";
                    return;
                }
                return {
                    good: $scope.model.good_selected,
                    NDS: $scope.model.NDS,
                    price_pre: $scope.model.price_pre,
                    price_post: $scope.model.price_post,
                    price_retail: $scope.model.price_retail,
                    price_gross: $scope.model.price_gross
                };
            };

            /*========================================================================================================*/

            if(!$scope.model) {
                $scope.model = {};
                $scope.isCollapsed = true;
            } else {
                $scope.model["good_selected"] = $scope.model.good;
                $scope.isCollapsed = false;
                $scope.getPrice();
                $scope.priceChange();
            }

            $scope.model.validate = {};
            $scope.model.errors = {};

            var func_fill = function() {
                if ($scope.model.price_retail && $scope.model.price_gross) {
                    $scope.fillclbk();
                } else {
                    $scope.unfillclbk();
                }
            };

            $scope.$watch('model.price_retail', function() {
                func_fill();
            });

            $scope.$watch('model.price_gross', function() {
                func_fill();
            });

//            $scope.loadGood = function(selected) {
//                GoodItems.query({}, function(data) {
//                    $scope.model.good_items = data.items;
//                    if (selected) {
//                        $scope.model.good_selected = selected;
//                    }
//                });
//            };

            $scope.resource = GoodItems.query;

//            $scope.loadGood();
        }
    };
})

.directive('goodEdit', function(CommodityItems, CommodityId, GoodItems, GoodItem) {
    return {
        restrict: 'E',
        scope: {
            object: "=",
            disabled: "=",
            savefnc: "=",
            successclbk: "="
        },
        templateUrl: '/static/template/goodbl/good-edit.html',
        controller: function($scope) {
            $scope.isCollapsedNumber = true;
            var isNumeric = false;
            var isNew = true;

            var isNumericCalc = function(numeric) {
                $scope.isCollapsedNumber = numeric ? false: true;
                isNumeric = numeric;
            };

            $scope.model = {};

            if($scope.object) {
                isNew = false;
                isNumericCalc($scope.object.commodity.numeric);
            } else {
                $scope.object = {};
            }

            $scope.model.commodity_items = {};

            $scope.model.validate = {};
            $scope.model.success = {};
            $scope.model.errors = {};
            $scope.model.errors.number_local = false;
            $scope.model.errors.number_global = false;

            $scope.commoditySelect = function (item, model) {
                isNumericCalc(item.numeric);
                if ($scope.object) {
                    $scope.object.number_global = undefined;
                    $scope.object.number_local = undefined;
                }
            };

            var setError = function(attr, message) {
                if (message) {
                    $scope.model.validate[attr] = message;
                    $scope.model.errors[attr] = true;
                } else {
                    $scope.model.validate[attr] = "";
                    $scope.model.errors[attr] = false;
                }
            };

            $scope.savefnc = function() {

                if (isNumeric) {
                    if(!$scope.object.number_local) {
                        setError("number_local", "Заполните поле номер в пределах года.");
                    } else {
                        setError("number_local");
                    }
                    if(!$scope.object.number_global) {
                        setError("number_global", "Заполните поле номер(общую).");
                    } else {
                        setError("number_global");
                    }
                }

                if(!$scope.object.commodity) {
                    setError("commodity", "Выберите запись");
                } else {
                    setError("commodity");
                }

                if (_.indexOf(_.values($scope.model.errors), true) != -1) {
                    return;
                }

                if (isNew) {
                    GoodItems.save({
                        data: {
                            commodity_id: $scope.object.commodity.id,
                            number_local: $scope.object.number_local,
                            number_global: $scope.object.number_global,
                            'price_id': undefined,
                            'price.price_retail': $scope.object['price.price_retail'],
                            'price.price_gross': $scope.object['price.price_gross']
                        }
                    }, function(data) {
                        $scope.successclbk(data);
                    }, function (data) {
                        $scope.model.validate.message = data.data.message;
                    });
                } else {
                    GoodItem.update({id: $scope.object.id, data: {
                        commodity_id: $scope.object.commodity.id,
                        number_local: $scope.object.number_local,
                        number_global: $scope.object.number_global,
                        'price_id': $scope.object.price_id,
                        'price.price_retail': $scope.object['price.price_retail'],
                        'price.price_gross': $scope.object['price.price_gross']
                    }}, function(data) {
                        $scope.successclbk(data);
                    });
                }
            };

//            $scope.loadCommodity = function(commodity) {
//
//                ({}, function(data) {
//                    $scope.model.commodity_items = data.items;
//                    if (commodity) {
//                        $scope.object.commodity = commodity;
//                        $scope.commoditySelect(commodity);
//                    }
//                });
//            };
//
//            $scope.loadCommodity();

            $scope.resource = CommodityItems.query;
        }
    };
});