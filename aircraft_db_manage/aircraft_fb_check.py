def check_model(self, app, model):
  meta = model._meta
  # Make a list of checks to run on each model instance
  checks = []
  for field in meta.local_fields + meta.local_many_to_many + meta.virtual_fields:
    if isinstance(field, models.ForeignKey):
      checks.append(check_foreign_key(model, field))

  # Run all checks
  fail_count = 0
  if checks:
    for instance in with_progress_meter(
        model.objects.all(), model.objects.count(),
        'Checking model %s ...' % model_name(model)):
      for check in checks:
        if not check(instance):
          fail_count += 1
  return fail_count
