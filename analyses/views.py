from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, ListView

from .forms import AnalysisCreateForm, AnalysisTitleForm
from .models import Analysis
from .tasks import generate_analysis


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("analysis-list")

    def form_valid(self, form: UserCreationForm) -> HttpResponse:
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class OwnedAnalysisMixin(LoginRequiredMixin):
    model = Analysis
    request: HttpRequest

    def get_queryset(self):
        return Analysis.objects.filter(owner_id=self.request.user.pk)


class AnalysisListView(LoginRequiredMixin, ListView):
    model = Analysis
    template_name = "analyses/analysis_list.html"
    context_object_name = "analyses"

    def get_queryset(self):
        user = self.request.user
        assert isinstance(user, User)
        queryset = Analysis.objects.filter(owner=user)
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(language__icontains=query)
                | Q(tags__icontains=query)
            )
        return queryset


class AnalysisCreateView(LoginRequiredMixin, CreateView):
    form_class = AnalysisCreateForm
    template_name = "analyses/analysis_form.html"

    def form_valid(self, form: AnalysisCreateForm) -> HttpResponse:
        user = self.request.user
        assert isinstance(user, User)
        form.instance.owner = user
        response = super().form_valid(form)
        assert self.object is not None
        generate_analysis.delay(str(self.object.pk))
        return response

    def get_success_url(self) -> str:
        assert self.object is not None
        return self.object.get_absolute_url()


class AnalysisDetailView(OwnedAnalysisMixin, DetailView):
    template_name = "analyses/analysis_detail.html"
    context_object_name = "analysis"


def owned_analysis(request: HttpRequest, pk) -> Analysis:
    return get_object_or_404(Analysis, pk=pk, owner=request.user)


@login_required
def analysis_status(request: HttpRequest, pk) -> HttpResponse:
    return render(
        request,
        "analyses/analysis_status.html",
        {"analysis": owned_analysis(request, pk)},
    )


@require_POST
@login_required
def update_title(request: HttpRequest, pk) -> HttpResponse:
    analysis = owned_analysis(request, pk)
    form = AnalysisTitleForm(request.POST, instance=analysis)
    if form.is_valid():
        form.save()
    return redirect("analysis-detail", pk=pk)


@require_POST
@login_required
def rate_analysis(request: HttpRequest, pk) -> HttpResponse:
    analysis = owned_analysis(request, pk)
    rating = request.POST.get("rating")
    if rating not in Analysis.Rating.values:
        return HttpResponseBadRequest("Nieprawidłowa ocena.")
    analysis.rating = rating
    analysis.save(update_fields=["rating", "updated_at"])
    return redirect("analysis-detail", pk=pk)


@require_POST
@login_required
def regenerate_analysis(request: HttpRequest, pk) -> HttpResponse:
    analysis = owned_analysis(request, pk)
    analysis.status = Analysis.Status.PENDING
    analysis.error_message = ""
    analysis.save(update_fields=["status", "error_message", "updated_at"])
    generate_analysis.delay(str(analysis.pk))
    return redirect("analysis-detail", pk=pk)


@require_POST
@login_required
def delete_analysis(request: HttpRequest, pk) -> HttpResponse:
    owned_analysis(request, pk).delete()
    return redirect("analysis-list")
