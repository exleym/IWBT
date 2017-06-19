
(function() {


    var app = angular.module("iwbtViewer", []);

    var MainCtrl = function ($scope, $http) {

        var onRequestComplete = function (response) {
            $scope.river = response.data
        };
        $http.get("/api/v1.0/river/1").then(onRequestComplete);
        $scope.message = "Hello, Angular!";
    };

    app.controller("MainCtrl", MainCtrl);

}());