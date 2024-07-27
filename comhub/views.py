from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from comhub.forms import QuestionForm, CommentForm
from .models import Question, Comment


def home(request):
    return render(request, 'comhub/home.html')

def about(request):
    return render(request, 'comhub/about.html')

def like_view(request, pk):
    post = get_object_or_404(Question, id=request.POST.get('question_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('comhub:question_detail', args=[str(pk)]))


def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user  # Assign the current user to the question
            question.save()
            return redirect('comhub:question_detail', pk=question.pk)  # Redirect to question detail page
    else:
        form = QuestionForm()
    
    return render(request, 'comhub/add_question.html', {'form': form})

def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    
    # Check if the user is the owner of the question
    if request.user == question.user:
        if request.method == 'POST':
            question.delete()
            # Redirect to a success page or another relevant page after deletion
            return redirect('comhub:question_list')  # Example: Redirect to question list
        else:
            return render(request, 'comhub/delete_question.html', {'question': question})
    else:
        # Handle cases where the user is not authorized to delete the question
        return HttpResponseForbidden("You do not have permission to delete this question.")
    
# def add_comment(request, pk):
#     question = get_object_or_404(Question, pk=pk)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.question = question
#             comment.save()
#             return redirect('comhub:question_detail', pk=pk)
#     else:
#         form = CommentForm()
#     return render(request, 'comhub/add_comment.html', {'form': form})
        
# def delete_comment(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     question_pk = comment.question.pk
#     if request.method == 'POST':
#         comment.delete()
#         return redirect('comhub:question_detail', pk=question_pk)
#     return render(request, 'comhub/delete_comment.html', {'comment': comment})

class CommentDetailView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comhub/question_detail.html'

    def form_valid(self, form):
        form.instance.question_id = self.kwargs['pk']
        return super().form_valid(form)
    
    success_url = reverse_lazy('comhub:question_detail')

class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comhub/add_comment.html'

    def form_valid(self, form):
        form.instance.question_id = self.kwargs['pk']
        return super().form_valid(form)
    
    success_url = reverse_lazy('comhub:question_list')


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'comhub/add_question.html'  # Use the same form template as add_question.html
    success_url = reverse_lazy('comhub:question_list')  # Redirect to question list upon successful update

    def form_valid(self, form):
        question = form.save(commit=False)
        question.user = self.request.user
        question.save()
        return redirect('comhub:question_detail', pk=question.pk)
    
    def dispatch(self, request, *args, **kwargs):
        # Get the question object
        self.object = self.get_object()

        # Check if the logged-in user is the owner of the question
        if self.object.user != self.request.user:
            return redirect('comhub:question_detail', pk=self.object.pk)  # Redirect to detail page if not owner
        
        return super().dispatch(request, *args, **kwargs)
    


class QuestionListView(ListView):
    model = Question
    context_object_name = 'questions'
    ordering = ['-date_created']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_input = self.request.GET.get('search_area') or ""
        if search_input:
            queryset = queryset.filter(title__icontains=search_input)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_input'] = self.request.GET.get('search_area') or ""
        return context

class QuestionDetailView(DetailView):
    model = Question

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionDetailView, self).get_context_data()
        something = get_object_or_404(Question, id=self.kwargs['pk'])
        total_likes = something.total_likes()
        liked = False
        if something.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['total_likes'] = total_likes
        context['liked'] = liked
        return context

# class QuestionUpdateView(UpdateView):
#     model = Question
#     field = ['title', 'content']





 