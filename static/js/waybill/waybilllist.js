var app = angular.module('myApp', ['ngRoute', 'ng-breadcrumbs', 'ngResource', 'ui.bootstrap', 'ngSanitize', 'ui.select', 'AuthModule', 'ngTable',
    'RestApp', 'TableHelper', 'FilterApp', 'Params', 'ModalApp', 'ElemsModule']);

app.controller("MainCtrl", function($scope, $route, $location, $routeParams) {
    $scope.$route = $route;
    $scope.$location = $location;
    $scope.$routeParams = $routeParams;
})

    .controller('WayBillsController', function($scope, $routeParams, $location, WayBillItems, ngTableParams, load, breadcrumbs) {
        $scope.breadcrumbs = breadcrumbs;
        $scope.model = {};

        $scope.select = function (selected) {
            $location.path("/admin/waybillcustomview/"+selected.id+"/edit");
        };

        $scope.resource = WayBillItems.query;
    })

    .controller('WayBillEditController', function($scope, $routeParams, $modal, WayBillItem, WayBillItemItems, DateWidgetScope,
                                              breadcrumbs, InvoiceItemHelper, wrapItemsToChangeCount) {
        $scope.breadcrumbs = breadcrumbs;

        $scope.model = {};

        $scope.model.date = {};

        $scope.model.items = [];
        $scope.model.waybill_id = $routeParams.id;
        $scope.isActionClmn = true;

        WayBillItemItems.query({id: $scope.model.waybill_id}, function(dt) {
            wrapItemsToChangeCount.wrapItems(dt.items, 3);
            $scope.model.items = dt.items;
        });

        $scope.removeFromInvoice = InvoiceItemHelper.removeFromInvoice;
        $scope.addToInvoice = InvoiceItemHelper.addToInvoice;

        WayBillItem.query({id: $scope.model.waybill_id}, function(data) {
            $scope.model.waybill = data;
            DateWidgetScope.wrapScope($scope.model.date);
            $scope.model.date.dt = data.date;
        });

        $scope.openToAdd = function () {

//            debugger

            var modalInstance = $modal.open({
                templateUrl: '/static/template/modalAddGood.html',
                controller: 'AddToController',
                resolve: {
                    pointsale_from_id: function() {return $scope.model.waybill.pointsale_from_id},
                    good_exclude: function() {return _.pluck($scope.model.items, 'good_id')}
                }
            });

            modalInstance.result.then(function (selected) {
                console.log(selected);
                $scope.model.items.push({
                    'full_name': selected.full_name,
                    'price_retail': selected.price_retail,
                    'price_gross': selected.price_gross,
                    'count': selected.count,
                    'price': $scope.model.waybill.type == 1 ? selected.price_retail : selected.price_gross,
                    'good_id': selected.good_id,
                    'is_approve': true
                });
                //$scope.calc_approve($scope.model.items);
                console.log("THEN1");
            }, function () {
                console.log("THEN2");
            });
        };

        $scope.saveAndPrint = function() {
            WayBillItem.save({id: $scope.model.waybill_id, data: {
                'items': $scope.model.items,
                'date': $scope.model.date.dt
            }}, function(resp) {
                var path = resp['path'];
                $scope.model.is_save = true;
                $scope.model.url_to_download = path;
                $scope.model.is_error = false;
                console.log("SAVE");
            }, function(resp) {
                $scope.model.message_error = resp.data['message'];
                $scope.model.is_save = false;
                $scope.model.is_error = true;
                console.log("ERROR");
            })
        };
    })

    .controller('WayBillFromAcceptanceCtrl', function($scope, $location, stateService, AcceptanceItems, ngTableParams, PointSaleItems,
                                                  ReceiverItems, DateWidgetScope, breadcrumbs, WayBillHelper, $rootScope) {
        $scope.breadcrumbs = breadcrumbs;

        $scope.model = {};

        $scope.model.acceptance = stateService.getStateAttr(stateService.ACCEPTANCE);
        $scope.model.pointsale_from = stateService.getStateAttr(stateService.POINTSALEFROM);
        $scope.model.mail = stateService.getStateAttr(stateService.MAIL);

        if(!$scope.model.acceptance && !$scope.model.pointsale_from && !$scope.model.mail) {
            $location.path("/admin/waybillcustomview");
            return
        }
        if ($scope.model.acceptance) {
            breadcrumbs.options = {'Создание новой накладной': 'Параметры накладной из ' + $scope.model.acceptance.pointsale_name + ' по приемке (' + $scope.model.acceptance.invoice_str + ')'};
        } else if ($scope.model.pointsale_from){
            breadcrumbs.options = {'Создание новой накладной': 'Параметры накладной из ' + $scope.model.pointsale_from.name};
        } else {
            breadcrumbs.options = {'Создание новой накладной': 'Параметры накладной по почте от ' + $scope.model.mail.provider + ' (' + $scope.model.mail.date + ")"};
        }

        if ($scope.model.acceptance && $scope.model.pointsale_from) {
            $scope.model.pointsale_id = $scope.model.acceptance ? $scope.model.acceptance.pointsale_id : $scope.model.pointsale_from.id;
        }

        //==================================================================================================================

        $scope.model.typeInvoice = 1;
        $scope.model.typeT = 1;

        //==================================================================================================================

        $scope.nextStep = function () {
            if(!$scope.model.date.dt) {
                $scope.setError("Заполните поле даты");
            }

            else if ($scope.model.typeT == 1 && !$scope.model.selected_pointsale) {
                $scope.setError("Выберите товарную точку");
            }

            else if ($scope.model.typeT == 2 && !$scope.model.selected_receiver) {
                $scope.setError("Выберите получателя");
            }
            else {
                $scope.setError(undefined);

                stateService.setStateAttr(stateService.TYPEINVOICE, $scope.model.typeInvoice);
                stateService.setStateAttr(stateService.DATE, $scope.model.date.dt);
                if ($scope.model.typeT == 1) {
                    stateService.setStateAttr(stateService.POINTSALE, $scope.model.selected_pointsale);
                    stateService.setStateAttr(stateService.RECEIVER, undefined);
                } else {
                    stateService.setStateAttr(stateService.RECEIVER, $scope.model.selected_receiver);
                    stateService.setStateAttr(stateService.POINTSALE, undefined);
                }

                var acceptance = stateService.getStateAttr(stateService.ACCEPTANCE);
                var receiver = stateService.getStateAttr(stateService.RECEIVER);
                var pointsale = stateService.getStateAttr(stateService.POINTSALE);
                var type = stateService.getStateAttr(stateService.TYPEINVOICE);

                if ($scope.model.acceptance) {
                    WayBillHelper.check({
                        invoice_id: acceptance.invoice_id,
                        receiver_id: receiver ? receiver.id : -1,
                        pointsale_id: pointsale ? pointsale.id : -1,
                        type: type ? type : - 1
                    }, function(data) {

                        var status = data['status'];

                        if (status) {

                            var data = data['data'];

                            var message = "";

                            if (receiver) {
                                message = "На выбранного получателя "+receiver.full_name+" уже есть сформированная накладная. Вы можете отредактировать ее или создать новую."
                            } else {
                                message = "На выбранную торговую точку "+pointsale.name+" уже есть сформированная накладная. Вы можете отредактировать ее или создать новую."
                            }

                            bootbox.dialog({
                            message: message,
                            title: "Внимание!",
                            buttons: {

                                change_: {
                                    label: "Выбрать другого получателя!",
                                    className: "btn-success",
                                    callback: function() {
                                    }
                                },

                                new_: {
                                    label: "Создать новую накладную!",
                                    className: "btn-warning",
                                    callback: function() {
                                        func_next(true);
                                    }
                                },
                                edit_: {
                                    label: "Редактировать!",
                                    className: "btn-primary",
                                    callback: function() {
                                        console.log("MAIN");
                                        $rootScope.$apply(function() {
                                            $location.path("/admin/waybillcustomview/" + data['id'] + "/edit");
                                        });
                                    }
                                }
                            }
                            });

                            } else if (!status || data['extra'] == 'multi') {
                                func_next(false);
                            }
                    });
                } else {
                    func_next(false);
                }
            }
        };

        var func_next = function(root) {
            if ($scope.model.acceptance) {
                if (root) {
                    $rootScope.$apply(function() {
                        $location.path("/admin/waybillcustomview/select_acceptance/new_acceptance/blank");
                    });
                } else {
                    $location.path("/admin/waybillcustomview/select_acceptance/new_acceptance/blank");
                }

            } else if ($scope.model.pointsale_from) {
                if (root) {
                    $rootScope.$apply(function() {
                        $location.path("/admin/waybillcustomview/select_point/new_acceptance/blank");
                    });
                } else {
                    $location.path("/admin/waybillcustomview/select_point/new_acceptance/blank");
                }
            } else {
                if(root) {
                    $rootScope.$apply(function() {
                        $location.path("/admin/waybillcustomview/select_mail/new_acceptance/blank");
                    });
                } else {
                    $location.path("/admin/waybillcustomview/select_mail/new_acceptance/blank");
                }
            }
        };

        //==================================================================================================================

        var func_points = function(params, func_succ, func_fail) {
            var par = _.extend({ exclude_point_id: $scope.model.pointsale_id }, params);
            PointSaleItems.query(par, func_succ, func_fail);
        };

        $scope.resource_pointsale = func_points;
        $scope.resource_receiver = ReceiverItems.query;

//        ({ exclude_point_id: $scope.model.pointsale_id }, function(data) {
//            $scope.model.pointsale_items = data.items;
//        });
//
//        ({ }, function(data) {
//            $scope.model.receiver_items = data.items;
//        });

        //==================================================================================================================

        $scope.model.errors = {};
        $scope.setError = function(message) {
            if (message) {
                $scope.model.errors.is_error = true;
                $scope.model.errors.error_message = message;
            } else {
                $scope.model.errors.is_error = false;
                $scope.model.errors.error_message = "";
            }
        };

        //==================================================================================================================

        $scope.model.date = {};

        DateWidgetScope.wrapScope($scope.model.date);

        //==================================================================================================================
    })
    .controller('WayBillBlankCtrl', function($scope, $location, $modal, stateService, AcceptanceRemainItems, WayBill,
                                             WayBillItem, wrapItemsToChangeCount, InvoiceItems, InvoiceItemHelper,
                                             breadcrumbs)
    {

        $scope.breadcrumbs = breadcrumbs;

        var acceptance = stateService.getStateAttr(stateService.ACCEPTANCE);
        var receiver = stateService.getStateAttr(stateService.RECEIVER);
        var pointsale = stateService.getStateAttr(stateService.POINTSALE);
        var date = stateService.getStateAttr(stateService.DATE);
        var typeInvoice = stateService.getStateAttr(stateService.TYPEINVOICE);
        var pointsale_from = stateService.getStateAttr(stateService.POINTSALEFROM);
        var mail = stateService.getStateAttr(stateService.MAIL);

        //console.log(acceptance);

        //$scope.model.acceptance = stateService.getStateAttr(stateService.ACCEPTANCE);
        //$scope.model.pointsale_from =

        if(!acceptance && !pointsale_from && !mail) {
            $location.path("/admin/waybillcustomview");
            return
        }

        //Тип означает, основание создания накладной(из приемки, из почты или кастомная)
        var type = "acceptance";
        if(mail) {
            type = "mail";
            $scope.addHide = true;
        } else if (pointsale_from) {
            type = "custom";
        }

        if(receiver) {
            breadcrumbs.options['БЛАНК'] = 'Формирование '+ (typeInvoice == 1? 'розничной' : 'оптовой') +' накладной ' + receiver.fullname;
        } else {
            breadcrumbs.options['БЛАНК'] = 'Формирование '+ (typeInvoice == 1? 'розничной' : 'оптовой') +' накладной в ' + pointsale.name;
        }

        $scope.saveAndPrint = function() {
            saveRetailInvoice();
        };

        $scope.model = {};
        $scope.model.items = [];

        $scope.model.typeInvoice = typeInvoice;

        if (acceptance) {
            $scope.isActionClmn = true;
            AcceptanceRemainItems.query({ id: acceptance.id }, function(data) {
                var items = data.items;
                wrapItemsToChangeCount.wrapItems(items, typeInvoice);
                $scope.model.items = items;
            });
        }

        if (mail) {
            $scope.isActionClmn = true;
            InvoiceItems.query({id: mail.invoice_id}, function(data) {
                var items = data.items;
                wrapItemsToChangeCount.wrapItems(items, typeInvoice);
                $scope.model.items = items;
            });
        }


        $scope.removeFromInvoice = InvoiceItemHelper.removeFromInvoice;
        $scope.addToInvoice = InvoiceItemHelper.addToInvoice;

        $scope.openToAdd = function () {

//            debugger

            var modalInstance = $modal.open({
                templateUrl: '/static/template/modalAddGood.html',
                controller: 'AddToController',
                resolve: {
                    pointsale_from_id: function() {return pointsale_from? pointsale_from.id : acceptance.pointsale_id},
                    good_exclude: function() {return _.pluck($scope.model.items, 'good_id')}
                }
            });

            modalInstance.result.then(function (selected) {
                console.log(selected);
                var el = {
                    'full_name': selected.full_name,
                    'price_retail': selected.price_retail,
                    'price_gross': selected.price_gross,
                    'count': selected.count,
                    'price': typeInvoice == 1 ? selected.price_retail : selected.price_gross,
                    'good_id': selected.good_id
                };
                $scope.model.items.push(el);
                //if(acceptance) {
                    wrapItemsToChangeCount.wrapItem(el);
                //} else {
                //    el.is_approve = true;
                //}
                //$scope.calc_approve($scope.model.items);
                console.log("THEN1");
            }, function () {
                console.log("THEN2");
            });
        };

        function saveRetailInvoice() {
            var res = $scope.model.items; //, function(elem){ return elem.is_approve; });

//            var method = force?'query_confirm':'query';
            if ($scope.model.is_save) {

                WayBillItem.save({
                    id: $scope.model.id,
                    data: {
                        date: date,
                        items: res
                    }
                }, function(data) {
                    var path = data['path'];
                    var status = data['status'];

                    if (status == "ok") {
//                        var data = resp['data'];
                        $scope.model.is_save = true;
                        $scope.model.url_to_download = path;
                        $scope.model.is_error = false;
//                        $scope.model.id = data['id'];
                        //loadItems();
                    } else {
                        throw Error("BLA");
                    }
                })

            } else {
                var inv_id = null, point_from_id = null;
                if (type == "acceptance") {
                    inv_id = acceptance.invoice_id;
                    point_from_id = acceptance.pointsale_id;
                } else if (type == "mail") {
                    inv_id = mail.invoice_id;
                } else {
                    point_from_id = point_from_id.id;
                }

                WayBill.query({
                    'data': {
//                        'typePl': type,
                        'invoice_id': inv_id,
                        'items': res,
                        'type': typeInvoice,
                        'receiver_id': receiver ? receiver.id : -1,
                        'pointsale_id': pointsale ? pointsale.id : -1,
                        'pointsale_from_id': point_from_id,
                        'date': date
                    }
                },
                function(resp) {
                    var path = resp['path'];
                    var status = resp['status'];

                    if (status == "ok") {
                        var data = resp['data'];
                        $scope.model.is_save = true;
                        $scope.model.url_to_download = path;
                        $scope.model.is_error = false;
                        $scope.model.id = data['id'];
                    } else {
                        throw Error("BLA");
                    }
                },
                function(resp) {
                    $scope.model.message_error = resp.data['message'];
                    $scope.model.is_save = false;
                    $scope.model.is_error = true;
                });
            }
        }

    })

    .controller('WayBillSelectAcceptanceCtrl', function($scope, $location, stateService, ngTableParams, AcceptanceItems, breadcrumbs) {
        $scope.breadcrumbs = breadcrumbs;
        $scope.model = {};
        $scope.selected = {};
        //==================================================================================================================
        $scope.nextStep = function () {
            stateService.setStateAttr(stateService.ACCEPTANCE, $scope.selected);
            stateService.setStateAttr(stateService.POINTSALEFROM, undefined);
            stateService.setStateAttr(stateService.MAIL, undefined);
            $location.path("/admin/waybillcustomview/select_acceptance/new_acceptance");
        };
        //==================================================================================================================
        $scope.resource = AcceptanceItems.query;
    })

    .controller('WayBillMailCtrl', function($scope, MailItems, breadcrumbs, $location, stateService) {
        $scope.breadcrumbs = breadcrumbs;

        $scope.setSelected = function(item) {
            stateService.setStateAttr(stateService.MAIL, item);
            stateService.setStateAttr(stateService.POINTSALEFROM, undefined);
            stateService.setStateAttr(stateService.ACCEPTANCE, undefined);
            $location.path("/admin/waybillcustomview/select_mail/new_acceptance");
        };

        $scope.resource = MailItems.query;
    })

    .controller('WayBillSelectPointCtrl', function ($scope, $location, stateService, PointSaleItems, breadcrumbs) {
        $scope.breadcrumbs = breadcrumbs;
        $scope.model = {};

        PointSaleItems.query({}, function(data) {
            $scope.model.pointsale_items = data.items;
        });

        $scope.nextStep = function() {
            stateService.setStateAttr(stateService.POINTSALEFROM, $scope.model.selected_pointsale);
            stateService.setStateAttr(stateService.ACCEPTANCE, undefined);
            $location.path("/admin/waybillcustomview/select_point/new_acceptance");
        };
    })

    .factory('stateService', function() {
        var POINTSALE = 'pointsale',
            POINTSALEFROM = 'pointsalefrom',
            RECEIVER = 'receiver',
            TYPEINVOICE = 'typeInvoice',
            ACCEPTANCE = 'acceptance',
            DATE = 'date',
            MAIL = 'mail';

        var state = {
            POINTSALE: undefined,
            POINTSALEFROM: undefined,
            RECEIVER: undefined,
            TYPEINVOICE: undefined,
            ACCEPTANCE: undefined,
            DATE: undefined
        };
        return {
                POINTSALE: POINTSALE,
                POINTSALEFROM: POINTSALEFROM,
                RECEIVER: RECEIVER,
                TYPEINVOICE: TYPEINVOICE,
                ACCEPTANCE: ACCEPTANCE,
                DATE: DATE,
                setState: function(st) {
                    state = st;
                },

                getState: function() {
                    return state;
                },

                setStateAttr: function (attr, value) {
                    state[attr] = value;
                },

                getStateAttr: function(attr) {
                    return state[attr];
                }
        }
    })

    .config(function($routeProvider, $locationProvider) {
      $routeProvider
          .when('/admin/waybillcustomview', {
              templateUrl: '/static/template/waybilllist.html',
              controller: 'WayBillsController',
              label: 'Список накладных'
          })
          .when('/admin/waybillcustomview/:id/edit', {
              templateUrl: '/static/template/waybilledit.html',
              controller: 'WayBillEditController',
              label: 'Редактирование'
          })

          .when('/admin/waybillcustomview/select_acceptance', {
              templateUrl: '/static/template/waybillselectacceptance.html',
              controller: 'WayBillSelectAcceptanceCtrl',
              label: 'Выбор приемки'
          })

          .when('/admin/waybillcustomview/select_mail', {
              templateUrl: '/static/template/waybill/from_mail.html',
              controller: 'WayBillMailCtrl',
              label: "Выбор письма"
          })

          .when('/admin/waybillcustomview/select_point', {
              templateUrl: '/static/template/waybillselectpoint.html',
              controller: 'WayBillSelectPointCtrl',
              label: 'Выбор точки-отправителя'
          })

          .when('/admin/waybillcustomview/select_acceptance/new_acceptance', {
              templateUrl: '/static/template/waybillfromacceptance.html',
              controller: 'WayBillFromAcceptanceCtrl',
              label: 'Создание новой накладной'
          })

          .when('/admin/waybillcustomview/select_point/new_acceptance', {
              templateUrl: '/static/template/waybillfromacceptance.html',
              controller: 'WayBillFromAcceptanceCtrl',
              label: 'Создание новой накладной'
          })

          .when('/admin/waybillcustomview/select_mail/new_acceptance', {
              templateUrl: '/static/template/waybillfromacceptance.html',
              controller: 'WayBillFromAcceptanceCtrl',
              label: "Создание новой накладной"
          })

          .when('/admin/waybillcustomview/select_acceptance/new_acceptance/blank', {
              templateUrl: '/static/template/waybillblank.html',
              controller: 'WayBillBlankCtrl',
              label: 'БЛАНК'
          })
          .when('/admin/waybillcustomview/select_point/new_acceptance/blank', {
              templateUrl: '/static/template/waybillblank.html',
              controller: 'WayBillBlankCtrl',
              label: 'БЛАНК'
          })
          .when('/admin/waybillcustomview/select_mail/new_acceptance/blank', {
              templateUrl: '/static/template/waybillblank.html',
              controller: 'WayBillBlankCtrl',
              label: 'БЛАНК'
          })

          .otherwise({
            redirectTo: '/admin/waybillcustomview'
          });


      // configure html5 to get links working on jsfiddle
      $locationProvider.html5Mode(true);
    });