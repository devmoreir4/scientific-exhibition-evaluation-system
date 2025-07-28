import BaseLayout from './components/BaseLayout.vue'

export default [
  {
    path: '/login',
    name: 'Login',
    component: () => import('./views/LoginView.vue'),
    meta: { public: true }
  },
  {
    path: '/',
    redirect: '/login'
  },
  // Rotas protegidas (admin)
  {
    path: '/admin',
    component: BaseLayout,
    meta: { requiresAuth: true, admin: true },
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('./views/AdminDashboardView.vue')
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('./views/AdminUsersView.vue')
      },
      {
        path: 'works',
        name: 'AdminWorks',
        component: () => import('./views/AdminWorksView.vue')
      },
      {
        path: 'sheets',
        name: 'AdminSheets',
        component: () => import('./views/AdminSheetsView.vue')
      }
    ]
  },
  // Rotas protegidas (avaliador)
  {
    path: '/',
    component: BaseLayout,
    meta: { requiresAuth: true, evaluator: true },
    children: [
      {
        path: 'dashboard',
        name: 'EvaluatorDashboard',
        component: () => import('./views/EvaluatorDashboardView.vue')
      },
      {
        path: 'evaluate/:work_id',
        name: 'EvaluationForm',
        component: () => import('./views/EvaluationFormView.vue')
      },
      {
        path: 'change-password',
        name: 'ChangePassword',
        component: () => import('./views/ChangePasswordView.vue')
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('./views/NotFoundView.vue')
  }
] 