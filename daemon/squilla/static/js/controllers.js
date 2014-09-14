'use strict';

/* Controllers */
var squilla_controllers = angular.module('squilla.controllers', [])

squilla_controllers.controller('IndexCtrl', ['$scope', '$http',
        function($scope, $http) {
            $http.get('/echo/sdag').success(function(data) {
                $scope.toto = data['echo'];
            });
    }])

    .controller('ConfigCtrl', ['$scope', '$http', 'messageCenterService',
        function($scope, $http, messageCenterService) {
            $http.get('/core/config').success(function(data) {
                $scope.config = data;
            });


        $scope.save = function(config) {
            $http.post('/core/config', config).success(function(data) {
                messageCenterService.add(data.state, data.message);
            });
        }

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
