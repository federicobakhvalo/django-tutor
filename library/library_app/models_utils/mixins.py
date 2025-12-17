class TailwindFormMixin:
    """
    Миксин для формы, который позволяет легко добавлять Tailwind классы
    ко всем виджетам через атрибут self.inputClass
    """
    inputClass = "w-full rounded-lg border border-gray-700 bg-[#191919] border-[#303030] text-white px-3 py-2 focus:outline-none"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{self.inputClass} {existing_classes}".strip()


class TitleContextMixin:
    title = None  # можно переопределять в view
    extra_context_data = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.title:
            context['title'] = self.title

        if self.extra_context_data:
            context.update(self.extra_context_data)

        return context