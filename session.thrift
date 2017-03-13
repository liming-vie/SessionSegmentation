struct SessSegRequest {
	1: list<string> context,
	2: string query
}

struct SessSegResponse {
	1: double score, # higher means not like a session
}

service SessionSegment {
	SessSegResponse calculate(1: SessSegRequest request)
}
