from django.urls import path
from number_system.view import user_views, admin_views, toolbox_views, question_generator_views, extra_views, \
    problem_solver_views, study_materials_views
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import views as auth_views
from number_system.view.subscription_view import *


urlpatterns = [

    path('', extra_views.homepage, name='homepage'),
    path('test/', extra_views.test, name='test'),
    # =============== Tool Box Views ===============
    path('tools/', toolbox_views.tools, name='tools'),
    path('base_converter/', toolbox_views.base_converter, name="base_converter"),
    path('base_calculator/', toolbox_views.base_calculator, name='base_calculator'),
    path('recursion_solver/', toolbox_views.recursion_solver, name='recursion_solver'),
    path('solve/recursion/', toolbox_views.solve_recursion, name="solve_recursion"),
    path('IDE/', toolbox_views.ide, name='ide'),
    path('ide/run/', toolbox_views.ide_run, name='ide_run'),
    path('prefix_infix_postfix/', toolbox_views.prefix_infix_postfix, name='prefix_infix_postfix'),
    path('solve/prefix_infix_postfix/', toolbox_views.prefix_infix_postfix_solver, name='prefix_infix_postfix_solver'),
    path('bit_string_flicking/', toolbox_views.bit_string_flicking, name='bit_string_flicking'),
    path('solve/bit_string_flicking/', toolbox_views.bit_string_flicking_solver, name='bit_string_flicking_solver'),
    path('solve/bit_string_flicking_equation/', toolbox_views.bit_string_flicking_equation_solver, name='bit_string_flicking_equation_solver'),

    # =============== Admin Views ===============
    path('admin-tools/problem-generator/', admin_views.problem_generator, name='admin_problem_generator'),
    path('generate/<str:question_type>/', admin_views.generate_questions, name='generate_question'),

    # =============== Problem Solver Views ===============
    path('problem_solver/', problem_solver_views.problem_solver, name='problem_solver'),
    path('ask-question/', problem_solver_views.ask_question, name='ask_question'),

    # =============== Question Generator Views ===============
    path('question_generator/', question_generator_views.question_generator_homepage,
         name='question_generator_homepage'),
    path('question_generator/<str:question_type>/', question_generator_views.question_generator,
         name='question_generator'),
    path('question/<str:pk>/', question_generator_views.view_question, name='view_question'),
    path('update/like/<str:pk>/', question_generator_views.like, name="like"),

    # =============== User Views ===============
    path('accounts/profile/', user_views.view_profile, name='profile'),
    path('accounts/profile/edit/', user_views.edit_profile, name='edit_profile'),
    path('accounts/profile/solver_profile', user_views.solver_profile, name='solver_profile'),
    path('accounts/profile/users/<str:username>/', user_views.view_user_profile, name='view_profile'),
    path('accounts/profile/users/<str:username>/solver_profile', user_views.view_user_solver_profile,
         name='view_solver_profile'),
    path('register/', user_views.UserRegisterView.as_view(), name='register'),
    path('login/', user_views.UserLoginView.as_view(), name='login'),
    # path('reset-password/', user_views.UserPasswordResetView.as_view(), name='reset_password'),
    # path('reset-password/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logout/', user_views.logout_user, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    # =============== Study Materials ===============
    path('study-materials/', study_materials_views.study_materials, name='study_materials'),
    path('study-materials/<str:topic>/', study_materials_views.study_materials_topic, name='study_materials_topic'),
    path('check-answer/<str:topic>/', study_materials_views.check_answer, name='check_answer'),

    # =============== Subscriptions =================
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
    path('subscription/create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('subscription/success/', SubscriptionSuccessView.as_view(), name='subscription_success'),
    path('subscription/cancel/', SubscriptionCancelView.as_view(), name='subscription_cancel'),
    path('stripe/webhook/', stripe_webhook, name='stripe_webhook'),

    # some changes in the branch
]
