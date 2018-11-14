from base.tests.factories.person import PersonFactory
from django.contrib.auth.models import Permission, Group


class UserMixin:

    @staticmethod
    def create_group(group_name):
        return Group.objects.get_or_create(name=group_name)

    @staticmethod
    def add_permissions_to_group(group_name, *permissions_names):
        group = Group.objects.get(name=group_name)
        for permission_name in permissions_names:
            permission = Permission.objects.get(codename=permission_name)
            group.permissions.add(permission)


class FacAdministratorMixin(UserMixin):
    def create_faculty_administrators_group(self):
        group, created = self.create_group('faculty_administrators')
        self.add_permissions_to_group('faculty_administrators', 'add_educationgroup')
        self.add_permissions_to_group('faculty_administrators', 'change_educationgroup')
        self.add_permissions_to_group('faculty_administrators', 'can_access_education_group')
        self.add_permissions_to_group('faculty_administrators', 'can_edit_educationgroup_pedagogy')
        self.add_permissions_to_group('faculty_administrators', 'change_educationgroup')
        self.add_permissions_to_group('faculty_administrators', 'delete_educationgroup')
        self.add_permissions_to_group('faculty_administrators', 'add_educationgroupachievement')
        self.add_permissions_to_group('faculty_administrators', 'change_educationgroupachievement')
        self.add_permissions_to_group('faculty_administrators', 'delete_educationgroupachievement')
        # self.add_permissions_to_group('faculty_administrators', 'is_entity_manager')
        self.add_permissions_to_group('faculty_administrators', 'change_learningclassyear')
        self.add_permissions_to_group('faculty_administrators', 'change_learningcomponentyear')
        self.add_permissions_to_group('faculty_administrators', 'can_access_learningunit')
        self.add_permissions_to_group('faculty_administrators', 'can_access_externallearningunityear')
        self.add_permissions_to_group('faculty_administrators', 'can_create_learningunit')
        self.add_permissions_to_group('faculty_administrators', 'can_delete_learningunit')
        self.add_permissions_to_group('faculty_administrators', 'can_edit_learningunit')
        self.add_permissions_to_group('faculty_administrators', 'can_edit_learningunit_date')
        self.add_permissions_to_group('faculty_administrators', 'can_edit_learningunit_pedagogy')
        self.add_permissions_to_group('faculty_administrators', 'can_edit_learningunit_specification')
        self.add_permissions_to_group('faculty_administrators', 'can_propose_learningunit')
        self.add_permissions_to_group('faculty_administrators', 'delete_learningunit')
        self.add_permissions_to_group('faculty_administrators', 'delete_learningunityear')
        self.add_permissions_to_group('faculty_administrators', 'can_access_catalog')
        self.add_permissions_to_group('faculty_administrators', 'can_access_offer')
        self.add_permissions_to_group('faculty_administrators', 'is_institution_administrator')
        # self.add_permissions_to_group('faculty_administrators', 'add_proposalfolder')
        # self.add_permissions_to_group('faculty_administrators', 'change_proposalfolder')
        # self.add_permissions_to_group('faculty_administrators', 'delete_proposalfolder')
        self.add_permissions_to_group('faculty_administrators', 'add_proposallearningunit')
        self.add_permissions_to_group('faculty_administrators', 'can_edit_learning_unit_proposal')
        self.add_permissions_to_group('faculty_administrators', 'change_proposallearningunit')
        self.add_permissions_to_group('faculty_administrators', 'delete_proposallearningunit')
        self.add_permissions_to_group('faculty_administrators', 'can_access_structure')
        self.add_permissions_to_group('faculty_administrators', 'add_externallearningunityear')
        return group

    def create_fac_admin(self, user=None):
        """
        Create a fac administrator person with all related objects and permissions
        :param user: related user object , if none it will be created
        :return: The fac administrator person
        """
        if user:
            person = PersonFactory(user=user)
        else:
            person = PersonFactory()
        faculty_admin_group = self.create_faculty_administrators_group()
        faculty_admin_group.user_set.add(person.user)
        return person
