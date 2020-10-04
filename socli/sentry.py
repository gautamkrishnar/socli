# Initialize Sentry
import sentry_sdk
from socli.version import __version__

sentry_sdk.init(
    "https://95c4106659044cbda2ea0fe499f4be7e@o323465.ingest.sentry.io/5445901",
    traces_sample_rate=1.0,
    release="socli-" + __version__
)

from socli.socli import main
main()
