
var app = angular.module('MailApp', ['ngResource', 'ui.bootstrap', 'ngSanitize', 'ui.select', 'AuthModule']);

app.controller("MailMainCtrl", function($scope) {
    $scope.model = {};
});