angular.module('myApp', ["ngRoute", "ngCookies", "ui.pagedown"])
	.config(['$routeProvider', function($routeProvider) {
		$routeProvider.when('/login', {
			template: '',
			controller: 'LoginCtrl'
		}).when('/reg', {
			templateUrl: 'tpl/user/reg.html',
			controller: 'RegCtrl'
		}).when('/index', {
			templateUrl: 'tpl/user/index.html',
			controller: 'IndexCtrl'
		}).when('/logout', {
			template: '',
			controller: 'LogoutCtrl'
		}).when('/change_pwd', {
			templateUrl: 'tpl/user/change_pwd.html',
			controller: 'ChangePwdCtrl'
		}).when('/tips', {
			templateUrl: 'tpl/user/tips.html',
			controller: 'TipsCtrl'
		}).when('/resumes_list', {
			templateUrl: 'tpl/user/resumes_list.html',
			controller: 'ResumesListCtrl'
		}).when('/resume/:groupId', {
			templateUrl: 'tpl/user/resume.html',
			controller: 'ResumeCtrl'
		}).when('/resume/:edit/:groupId', {
			templateUrl: 'tpl/user/resume.html',
			controller: 'ResumeCtrl'
		}).when('/new_pwd/:token', {
			templateUrl: 'tpl/user/new_pwd.html',
			controller: 'NewPwdCtrl'
		
		}).when('/hr', {
			templateUrl: 'tpl/hr/list.html',
			controller: 'HrListCtrl'
		}).when('/hr/logout', {
			template: '',
			controller: 'HrLogoutCtrl'
		}).when('/hr/resume/:id', {
			templateUrl: 'tpl/hr/resume.html',
			controller: 'HrResumeCtrl'
		}).when('/hr/:groupId', {
			templateUrl: 'tpl/hr/list.html',
			controller: 'HrListCtrl'

		}).when('/group/index', {
			redirectTo: '/group/resume_list/'
		}).when('/group/new_pwd/:token', {
			templateUrl: 'tpl/group/new_pwd.html',
			controller: 'GroupNewPwdCtrl'
		}).when('/group/join/', {
			templateUrl: 'tpl/group/join.html',
			controller: 'GroupJoinCtrl'
		}).when('/group/login/', {
			template: '',
			controller: 'GroupLoginCtrl'
		}).when('/group/login/:groupId', {
			template: '',
			controller: 'GroupLoginCtrl'
		}).when('/group/resume_list/', {
			templateUrl: 'tpl/group/resume_list.html',
			controller: 'GroupResumeListCtrl'
		}).when('/group/resume/:id', {
			templateUrl: 'tpl/group/resume.html',
			controller: 'GroupResumeCtrl'
		}).when('/group/change_pwd', {
			templateUrl: 'tpl/group/change_pwd.html',
			controller: 'GroupChangePwdCtrl'
		}).when('/group/change_pwd/:token', {
			templateUrl: 'tpl/group/change_pwd.html',
			controller: 'GroupChangePwdCtrl'
		}).when('/group/tips', {
			templateUrl: 'tpl/group/tips.html',
			controller: 'GroupTipsCtrl'
		}).when('/group/admin_list/', {
			templateUrl: 'tpl/group/admin_list.html',
			controller: 'GroupAdminListCtrl'
		}).when('/group/auth_code/', {
			templateUrl: 'tpl/group/auth_code.html',
			controller: 'GroupAuthCodeCtrl'
		}).when('/group/logout', {
			template: '',
			controller: 'GroupLogoutCtrl'
		}).when('/group', {
			redirectTo: '/group/resume_list/'
		}).otherwise({redirectTo: '/index'});
	}]);