angular.module('ElemsModule', [])

    .directive("topPanel", function() {
        return {
            restrict: "E",
            templateUrl: "/static/template/elems/topPanel.html",
            transclude: true,
            scope: {
                breadcrumbs: "="
            }
        }
    })

    .directive("searchField", function() {
            return {
                restrict: "E",
                templateUrl: "/static/template/elems/searchField.html",
                scope: {
                    placeholder: "@",
                    clbkclick: "="
                }
            }
    })

    .directive("dateField", function() {
        return {
            restrict: "E",
            templateUrl: "/static/template/elems/date.html",
            scope: {
                label: "@",
                model: "=",
                disabled: "="
            },
            controller: function($scope) {
                $scope.today = function() {
                    $scope.model.dt = new Date();
                };
                if (!$scope.model.dt) {
                    $scope.today();
                }


                $scope.clear = function () {
                    $scope.model.dt = null;
                };

                //scope.;

                $scope.disabledDate = function(date, mode) {
                    return ( mode === 'day' && ( date.getDay() === 0 || date.getDay() === 6 ) );
                };

                $scope.toggleMin = function() {
                    $scope.model.minDate = $scope.model.minDate ? null : new Date();
                };
                $scope.toggleMin();

                $scope.open = function($event) {
                    $event.preventDefault();
                    $event.stopPropagation();

                    $scope.opened = true;
                };

                $scope.dateOptions = {
                    formatYear: 'yy',
                    startingDay: 1
                };

                $scope.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
                $scope.format = $scope.formats[0];
            }
        }
    })

    .directive("tableRemote", function (ngTableParams, load, $compile) {
        return {
            restrict: "E",
            transclude: "element",
            scope: {
                "class": "@",
                resource: "=",
                selected: "=",
                handlerclkrow: "=",
                load: "=",
                filterField: "@"
            },
            priority: 1000,
            controller: function($scope) {
                $scope.model = {};

                $scope.model.filter_field = $scope.filterField;

                if ($scope.selected) {
                    $scope.setSelected = function (selected) {
                       $scope.model.idSelected = selected.id;
                       $scope.model.selected = selected;
                        $scope.selected = selected;
                    };
                    $scope.model.idSelected = null;
                }

                $scope.tableParams = new ngTableParams({
                    page: 1,            // show first page
                    count: 10,
                    sorting: {
                             // initial sorting
                    }
                }, {
                    counts: [],
                    total: 0,           // length of data
                    getData: function($defer, params) {

                        $scope.model.count = params.count();

                        $scope.model.page = params.page();

                        load.loadData(function(data) {
                            params.total(data.max);
                            $defer.resolve(data.items);
                        }, $scope.resource, {}, $scope);
                    }
                });

                $scope.load = function(text) {
                    $scope.model.filter_text = text;
                    $scope.tableParams.reload();
                };
            },
            link: function(scope, iElement, iAttrs, controller, transcludeFn) {

                var attrReplace = function(el, attr) {
                    if (attr.name.length > 2 && attr.name.substring(0, 2) == "r-") {
                        el.attr("ng-" + attr.name.substring(2, attr.name.length), el.attr(attr.name));
                    }
                };

                var attrRec = function(el) {
                    angular.forEach(el.children(), function(ch) {
                        var attrs = ch.attributes;
                        ch = angular.element(ch);
                        angular.forEach(attrs, function(attr) {
                            attrReplace(ch, attr);
                        });
                    })
                };

                var els = transcludeFn();
                var tr = angular.element("<tr></tr>");

                if(scope.handlerclkrow) {
                    tr.attr("ng-click", "handlerclkrow(item)")
                } else if (scope.selected) {
                    tr.attr("ng-click", "setSelected(item)");
                }

                var row = els.find("row");
                var attrs = row[0].attributes;

                angular.forEach(attrs, function(at) {
                    tr.attr(at.name, row.attr(at.name));
                    attrReplace(tr, at);
                });
                var tds = els.find("row > column");

                angular.forEach(tds, function(td) {
                    var tdnew = angular.element("<td></td>");
                    var attrs = td.attributes;

                    angular.forEach(attrs, function(at) {
                        tdnew.attr(at.name, angular.element(td).attr(at.name));
                        attrReplace(tdnew, at);
                    });

                    tdnew.append(td.children);
                    attrRec(tdnew);
                    tr.append(tdnew);
                });

                var columns_count = tds.length;

                var table = angular.element("<table ng-cloak ng-table=\"tableParams\" class=\"{{ class }}\"></table>");
                var tbody = angular.element("<tbody><tr ng-repeat=\"it in [] | range: 4 - $data.length\"><td colspan="+ columns_count +">&nbsp;</td></tr></tbody>");
                var tfoot = angular.element("<tfoot><tr></tr></tfoot>");
                table.append(tbody);
                table.append(tfoot);
                tbody.prepend(tr);

                iElement.after(table);

                $compile(table, transcludeFn)(scope);
            }
        }
    })

    .directive('dictSelectField', function() {
        return {
            restrict: 'E',
            templateUrl: '/static/template/elems/dictSelectField.html',
            scope: {
                label: '@',
                placeholder: '@',
                modal: '=',
                attrdisplay: '@',
                selected: "=",
                onSelect: "=",
                clbkclose: "=",
                disabled : "=",
                resource: "="
            },
            controller: function($scope, $modal) {
                $scope.edit = function() {
                    if ($scope.selected) {
                        $scope.createNew(false);
                    }
                };

                $scope.refresh = function(text){
                    $scope.reload(text);
                };

                if (angular.isUndefined($scope.disabled)) {
                    $scope.disabled = false;
                }
                $scope.modalMode = true;
                if($scope.modal) {
                    $scope.modalMode = false;
                    var template = $scope.modal[0];
                    var ctrl = $scope.modal[1];
                    var size = $scope.modal.length > 2 ? $scope.modal[2] : 'sm';
                }

                $scope.createNew = function(create) {
                    if ($scope.modal) {
                        var modalInstance;
                        if (create) {
                            modalInstance = $modal.open({
                                templateUrl: template,
                                controller: ctrl,
                                size: size,
                                resolve: {
                                    object: function() {
                                        return undefined;
                                    }
                                }
                            });
                        } else {
                            modalInstance = $modal.open({
                                templateUrl: template,
                                controller: ctrl,
                                size: size,
                                resolve: {
                                    object: function() {
                                        return $scope.selected;
                                    }
                                }
                            });
                        }

                        modalInstance.result.then(function (selected) {
            //                $scope.model.commodity_items.push(selected);
                            $scope.clbkclose(selected);
                        }, function () {
                            console.log("THEN2");
                        });
                    }

                };

                $scope.reload = function(text) {
                    if($scope.resource) {
                        $scope.resource({page: 1, count: 10, filter_text: text, filter_field: 'filter_field'}, function(data) {
                            $scope.items = data.items;
                        });
                    }
                };
            },
            link: function($scope, element, attrs) {
                $scope.someFunction = function(obj1, obj2) {
                    $scope.selected = obj1;
                    if ($scope.onSelect) {
                        $scope.onSelect(obj1, obj2);
                    }
                };
            }
        }
    });