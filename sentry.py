import sentry_sdk


def run_sentry():
    sentry_sdk.init(
        dsn="https://30886ff179a58f915d163a1c5ba6661c@o4507895344988160.ingest.de.sentry.io/4507895347413072",
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )
