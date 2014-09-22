/* Controllers */


squilla_controllers.controller('SMSHomeCtrl', ['$scope', '$http', 'messageCenterService',
        function($scope, $http) {
            $http.get('/sms/home').success(function(data) {
                $scope.config = data['config'];
            });
    }]);

squilla_controllers.controller('SMSConfigCtrl', ['$scope', '$http', 'messageCenterService',
        function($scope, $http) {
            // Get config
            $scope.load_config = function() {
                $http.get('/sms/config/load').success(function(data) {
                    $scope.config = data;
                });
            }

            // Get service status
            $scope.get_status = function() {
                $http.get('/sms/status').success(function(data) {
                    $scope.sms_status = data['status'];
                });
            }
            // Start service
            $scope.start = function() {
                $http.post('/sms/start').success(function(data) {
                    $scope.ret = data['status'];
                    $scope.get_status();
                });
            }

            // Stop service
            $scope.stop = function() {
                $http.post('/sms/stop').success(function(data) {
                    $scope.ret = data['status'];
                    $scope.get_status();
                });
            }

            // Restart service
            $scope.restart = function() {
                $scope.stop()
                $scope.start()
                $scope.get_status();
            }

            // Save configuration
            $scope.config_save = function(config) {
                $http.post('/sms/config/save', config).success(function(data) {
                    messageCenterService.add(data.state, data.message); 
                });
            }
            // Save config and restart
            $scope.config_save_restart = function(config) {
                $scope.config_save(config)
                $scope.restart()
            }
            // Get bonjour users
            $scope.get_bonjour_users = function() {
                $http.get('/sms/bonjour/users/get').success(function(data) {
                    $scope.presence_users = data
                });
            }


            $scope.get_status();
            $scope.load_config();
            $scope.get_bonjour_users()
    }]);
