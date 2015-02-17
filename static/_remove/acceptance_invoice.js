
var app = angular.module('AcceptanceApp', ['ngResource', 'ui.bootstrap', 'ngSanitize', 'ui.select', 'AuthModule', 'NumberApp',
    'RestApp']);

app.controller("MainCtrl", function($scope, InvoiceItemsFromMail, AcceptanceInvoiceItem) {
    $scope.model = {};

    $scope.model.date = {};

    $scope.model.errors = {};
    $scope.model.validate = {};


    $scope.model.date.today = function() {
        $scope.model.date.dt = new Date();
    };
    $scope.model.date.today();

    $scope.model.date.clear = function () {
        $scope.model.date.dt = null;
    };

    $scope.model.date.maxDate = '2015-06-22';

    $scope.model.date.disabled = function(date, mode) {
        return ( mode === 'day' && ( date.getDay() === 0 || date.getDay() === 6 ) );
    };

    $scope.model.date.toggleMin = function() {
        $scope.model.date.minDate = $scope.model.date.minDate ? null : new Date();
    };
    $scope.model.date.toggleMin();

    $scope.model.date.open = function($event) {
        $event.preventDefault();
        $event.stopPropagation();

        $scope.model.date.opened = true;
    };

    $scope.model.date.dateOptions = {
        formatYear: 'yy',
        startingDay: 1
    };

    $scope.model.date.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
    $scope.model.date.format = $scope.model.date.formats[2];

    InvoiceItemsFromMail.query({id: MAIL_ID}, function(data) {
        $scope.model.items = data.items;
    });

    $scope.saveAcceptance = function() {

        $scope.model.errors.date = $scope.model.date.dt ? false : true;

        if($scope.model.errors.date) {
            return;
        }

//        console.log(INVOICE_ID);
//        console.log(POINTSALE_ID);
        AcceptanceInvoiceItem.query({point_id: POINTSALE_ID, id: INVOICE_ID, 'data': {
            'items': $scope.model.items,
            'date': $scope.model.date.dt
        }}, function(data) {
//            console.log(data);
            $scope.model.validate.is_error = false;
            $scope.model.validate.is_success = true;
        }, function(data) {
//            console.log(data.data.message);
            $scope.model.validate.is_error = true;
            $scope.model.validate.error = data.data.message;
            $scope.model.validate.is_success = false;
        })
    };

});

