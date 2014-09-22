
squilla_app.config(['$routeProvider', function($routeProvider) {

        $routeProvider.when('/sms/home', {templateUrl: '/static/harbour-squilla-module-sms/partials/home.html', controller: 'SMSHomeCtrl'});
        $routeProvider.when('/sms/config', {templateUrl: '/static/harbour-squilla-module-sms/partials/config.html', controller: 'SMSConfigCtrl'});

    }]);


