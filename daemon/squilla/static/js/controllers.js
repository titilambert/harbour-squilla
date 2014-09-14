'use strict';

/* Controllers */
var squilla_controllers = angular.module('squilla.controllers', [])

squilla_controllers.controller('IndexCtrl', ['$scope', '$http',
        function($scope, $http) {
            $http.get('/echo/sdag').success(function(data) {
                $scope.toto = data['echo'];
            });
    }])

    .controller('EchoCtrl', ['$scope', '$http',
        function($scope, $http) {
            $scope.send = function(text) {
            
                if (text != null) {
                    $http.get('/echo/' + text).success(function(data) {
                        $scope.response = data['echo'];
                    });
                }
            }
    }])

    .controller('MenusCtrl', ['$scope', '$http',
        function($scope, $http) {
            $http.get('/menus').success(function(data) {
                $scope.menus = data['menus'];
            });
    }])

    .controller('ModulesCtrl', ['$scope', '$http',
        function($scope, $http) {
            $http.get('/core/modules').success(function(data) {
                $scope.modules = data['modules'];
            });
    }])
