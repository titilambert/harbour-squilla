'use strict';

var squilla_app = angular.module('Squilla', ['ngRoute',
                                             'squilla.controllers', 
                                             'MessageCenterModule'
                                            ]
                                );

squilla_app.config(['$routeProvider', function($routeProvider) {

        $routeProvider.when('/', {templateUrl: '/static/core/partials/index.html', controller: 'IndexCtrl'});
        $routeProvider.when('/core/config', {templateUrl: '/static/core/partials/config.html', controller: 'ConfigCtrl'});
        $routeProvider.when('/core/echo', {templateUrl: '/static/core/partials/echo.html', controller: 'EchoCtrl'});
        $routeProvider.when('/core/menus', {templateUrl: '/static/core/partials/menus.html', controller: 'MenusCtrl'});
        $routeProvider.when('/core/modules', {templateUrl: '/static/core/partials/modules.html', controller: 'ModulesCtrl'});
        $routeProvider.otherwise({redirectTo: '/'});

    }]);

