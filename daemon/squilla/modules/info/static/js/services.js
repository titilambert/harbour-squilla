

squilla_controllers.controller('NetworkCtrl', ['$scope', '$http',
        function($scope, $http) {
            $http.get('/info/networks').success(function(data) {
                $scope.networks = data['networks'];
            });
    }]);


