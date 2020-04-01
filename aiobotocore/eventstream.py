from botocore.eventstream import EventStream, EventStreamBuffer


class AioEventStream(EventStream):
    async def _create_raw_event_generator(self):
        event_stream_buffer = EventStreamBuffer()
        async for chunk, _ in self._raw_stream.iter_chunks():
            event_stream_buffer.add_data(chunk)
            for event in event_stream_buffer:
                yield event

    def __iter__(self):
        raise NotImplementedError('Use async-for instead')

    def __aiter__(self):
        return self.__anext__()

    async def __anext__(self):
        async for event in self._event_generator:
            parsed_event = self._parse_event(event)
            if parsed_event:
                yield parsed_event