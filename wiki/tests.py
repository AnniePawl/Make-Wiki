from django.test import TestCase
from django.utils.text import slugify
from django.contrib.auth.models import User 
from wiki.models import Page

# Canary Test
class WikiTestCase(TestCase):
  def true_true_is_true(self):
    '''tests if true equals true'''
    self.assertEqual(True,True)

# Test Details Page
  def test_details_page(self):
    # Create an instance of Page and save it to the database. (HINT: You’ll need to first create an instance of User to use as the page’s author.)
    user = User.objects.create()

    # Create and save a new page to the test database.
    page = Page.objects.create(
      title = "Starburst",
      content = "Introduced in 1960. Unexplainably Juicy",
      author = user 
     )
    page.save()

    # Load the Wiki Details page for that Page‘s slug.
    res = self.client.get(f'/{slugify(page.title)}/')

    # Verify that the response has a status_code of 200.
    self.assertEquals(res.status_code, 200)

    # Verify that the response’s context includes the info for the Page object requested. (HINT: You can use assertContains to check the exact text of the response.)
    self.assertContains(res, "Starburst")

# Test Details Edit 
  def test_details_edit(self):
    user = User.objects.create()
    # create instance of Page and save it to db 
     
    # Create dict of key-value pairs containing post data to be sent via form. Should include new page title and description
    page = Page.objects.create(
      title = "Cookie Monster",
      content = "Eats lots of cookies",
      author = user 
     )
    page.save()

    # Edit data 
    post_data = {

    }

    # Make POST request to details page w/ self.client.post()
    res = self.client.post()

    # Check that we get 302 status code 
    self.assertEqual(res.status_code, 302)

    # Check that page object was modified in test db 
    edited_data= Page.objects.get(title= [post_data['title']])
    self.assertEqual(edited_data.title, 'Cookie Monster')

# Test Creation Page 
  def test_create_page(self):
    user = User.objects.create()

    # Create dict of key-value pairs containing data to be sent via form. Should include page title and description n

    # Make POST request to wiki create page w/ self.client.post()

    # Check that page object was created in test db 