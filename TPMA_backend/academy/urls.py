# academy/urls.py

app_name = 'academy'

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProgramViewSet

from .views import (
    DesignationAPIView,
    TermChoicesAPIView,
    InstituteAPIView,  
    DepartmentAPIView,
    DegreeTypeAPIView,
    SupervisorEnrollmentAPIView,
    EnrolledSupervisorRetrieveView,
    ProgramViewSet,
    SemesterViewSet,
    OpenSemesterAPIView,
    CourseViewSet,
    BatchViewSet,
    BatchActiveViewSet,
    BatchesByProgramAPIView,
    SectionViewSet,
    SectionByBatchAPIView,
    TraineeEnrollmentAPIView,
    ProgramAPIView,
    CourseOfferAPIView,
    CourseOfferListFilteredView,
    CourseEnrollmentView,
    MarksheetViewSet,
    CheckCourseEnrollments,
    TraineeEnrolledCoursesAPIView,
    TraineesInCourseOfferView,
    MarksheetListByCourseOffer,
    CourseOfferCommentsView,
    AcademicRecordsAPIView,
  LessonPlanView, ReportView, AssessmentView, AILessonPlanView

)

router = DefaultRouter()
router.register(r'programs', ProgramViewSet)
router.register(r'semesters', SemesterViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'batches', BatchViewSet)
router.register(r'active-batches', BatchActiveViewSet)
router.register(r'sections', SectionViewSet)
router.register(r'marksheets', MarksheetViewSet)


urlpatterns = [
    path('designations/', DesignationAPIView.as_view(), name='designations'),
    path('designations/<int:pk>/', DesignationAPIView.as_view(), name='designation-pk'),
    path('term-choices/', TermChoicesAPIView.as_view(), name='term-choices'),
    path('term-choices/<int:pk>/', TermChoicesAPIView.as_view(), name='term-choice-pk'),
    path('institutes/', InstituteAPIView.as_view(), name='institutes'),  
    path('institutes/<int:pk>/', InstituteAPIView.as_view(), name='institute-pk'),  
    path('departments/', DepartmentAPIView.as_view(), name='departments'),  
    path('departments/<int:pk>/', DepartmentAPIView.as_view(), name='department-pk'),  
    path('open-semesters/', OpenSemesterAPIView.as_view(), name='open_semesters'), 
    path('degree-types/', DegreeTypeAPIView.as_view(), name='degree-types'),  
    path('degree-types/<int:pk>/', DegreeTypeAPIView.as_view(), name='degree-type-pk'),  
    path('programs/get/<int:program_id>/', ProgramAPIView.as_view(), name='get-program'),
    path('supervisor-enrollment/', SupervisorEnrollmentAPIView.as_view(), name='supervisor-enrollment'),  
    path('supervisor-enrollment/<int:pk>/', SupervisorEnrollmentAPIView.as_view(), name='supervisor-enrollment-pk'),  
    path('get-enrolled-supervisor/', EnrolledSupervisorRetrieveView.as_view(), name='get-enrolled-supervisor'),  
    path('trainee-enrollment/', TraineeEnrollmentAPIView.as_view(), name='trainee-enrollment'),  
    path('trainee-enrollment/<int:enrollment_id>/', TraineeEnrollmentAPIView.as_view(), name='trainee-enrollment-pk'),  
    path('trainees/<int:trainee_id>/enrollment/', TraineeEnrollmentAPIView.as_view(), name='trainee-id-enrollment'),
    path('batches/program/<int:program_id>/', BatchesByProgramAPIView.as_view(), name='batches-of-program'),  
    path('sections/batch/<int:batch_id>/', SectionByBatchAPIView.as_view(), name='sections-of-batch'),  
    path('course-offers/', CourseOfferAPIView.as_view(), name='course-offer'),
    path('course-offers/<int:pk>/', CourseOfferAPIView.as_view(), name='course-offer-detail'),
    path('supervisor/<int:supervisor_id>/course_offers/', CourseOfferListFilteredView.as_view(), name='course_offers_by_supervisor'),
    path('semester/<int:semester_id>/course_offers/', CourseOfferListFilteredView.as_view(), name='course_offers_by_semester'),
    path('course-enrollment/', CourseEnrollmentView.as_view(), name='course_enrollment'),
    path('course-enrollment/<int:pk>/', CourseEnrollmentView.as_view(), name='course_enrollment_detail'),
    path('course/check-enrollments/<int:course_id>/<int:trainee_id>/', CheckCourseEnrollments.as_view(), name='check_enrollments'),
    path('trainee/<int:trainee_id>/enrollments/', TraineeEnrolledCoursesAPIView.as_view(), name='trainee_enrollments'),
    path('course_offer/<int:course_offer_id>/trainees/', TraineesInCourseOfferView.as_view(), name='trainees_in_course_offer'),
    path('course-offer/marksheets/<int:course_offer_id>/', MarksheetListByCourseOffer.as_view(), name='marksheet-list-by-course-offer'),
    path('courseoffer/<int:course_offer_id>/comments/', CourseOfferCommentsView.as_view(), name='course_offer_discussion_comment'),
    path('trainees/<int:trainee_id>/academic-records/', AcademicRecordsAPIView.as_view(), name='trainee_academic_records_for_satff'),
    path('trainees/<int:trainee_id>/academic-records/<int:pk>/', AcademicRecordsAPIView.as_view(), name='trainee_academic_record_for_satff'),
    


    path('lesson-plans/', LessonPlanView.as_view(), name='lesson_plans'),
    path('reports/', ReportView.as_view(), name='reports'),
    path('assessments/', AssessmentView.as_view(), name='assessments'),
    path('ai/lesson-plan/', AILessonPlanView.as_view(), name='ai_lesson_plan'),
    
    
    
    path('', include(router.urls)),
]

