from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import Event, ReadableSpan, TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SpanExporter
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from strands.telemetry import StrandsTelemetry

ENTITIES = ["EMAIL_ADDRESS", "PHONE_NUMBER", "CREDIT_CARD", "US_SSN", "IBAN_CODE", "IP_ADDRESS"]
_analyzer = AnalyzerEngine()
_anonymizer = AnonymizerEngine()


def redact_text(value):
    if not isinstance(value, str) or not value:
        return value
    found = _analyzer.analyze(text=value, language="en", entities=ENTITIES)
    return _anonymizer.anonymize(text=value, analyzer_results=found).text if found else value


class RedactingExporter(SpanExporter):
    """Copies each span with PII replaced, then hands it to the real exporter."""

    def __init__(self, inner):
        self.inner = inner

    @staticmethod
    def _attrs(attrs):
        return {k: redact_text(v) for k, v in (attrs or {}).items()}

    def export(self, spans):
        cleaned = [ReadableSpan(
            name=s.name, context=s.context, parent=s.parent, resource=s.resource,
            attributes=self._attrs(s.attributes),
            events=[Event(e.name, self._attrs(e.attributes), e.timestamp) for e in s.events],
            links=s.links, kind=s.kind, status=s.status, start_time=s.start_time,
            end_time=s.end_time, instrumentation_scope=s.instrumentation_scope,
        ) for s in spans]
        return self.inner.export(cleaned)

    def shutdown(self):
        self.inner.shutdown()


def setup_telemetry():
    provider = TracerProvider()
    provider.add_span_processor(BatchSpanProcessor(RedactingExporter(OTLPSpanExporter())))
    trace.set_tracer_provider(provider)
    StrandsTelemetry(tracer_provider=provider)
