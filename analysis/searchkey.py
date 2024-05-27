REGEX = {
        # numeric
        'division by zero':r'div(i(de|sion)(s)?)?.by.(zero|0)', # CWE-369
        'integer truncation':r'int(eger)?.truncation', # CWE-197
        'integer overflow':r'int(eger)?.overflow', # CWE-190
        'floating point exception':r'floating.point.exception|\bfpe\b',
        # memory
        'out of memory':r'out(side)?.of.memory|\boom\b',
        'memory leak':r'(data|memory).leak',
        'memory corruption':r'(data|memory).corruption|bad.alloc',
        'infinite loop':r'infinite.loop',
        'invalid memory access':r'invalid.memory.access|access.(\w+.)?invalid.memory|write.(\w+.)?immutable.memory|access.(\w+.)?undefined.memory',
        'arbitrary memory access':r'arbitrary.memory.(read|write|access)',
        'null pointer dereference':r'null(.)?(pointer|ptr)?(.)?deref(erence)?|deref(erenc(e|ing))?.of.null(.)?(pointer|ptr)?',
        'reference binding to null pointer':r'reference.binding.to.null(.)?(.)?(pointer|ptr)?',
        'null pointer exception':r'null(.)?(pointer|ptr)?(.)?exception|\bnpe\b',
        'use after free':r'use.after.free', # CWE-416
        # buffer
        'heap buffer overflow':r'heap.(buffer.)?overflow|out.of.buffer', # CWE-122
        'stack overflow':r'stack.overflow(?!.com)', # CWE-121
        'out of bound read':r'(heap.)?(out(side)?.of.bound(s)?|\boob\b).read|read.(out(side)?.of.bound(s)?|\boob\b)', # CWE-125
        'out of bound write':r'(heap.)?(out(side)?.of.bound(s)?|\boob\b).write|write.(out(side)?.of.bound(s)?|\boob\b)', # CWE-787
        'out of bound access':r'(heap.)?(out(side)?.of.bound(s)?|\boob\b).access|access.(out(side)?.of.bound(s)?|\boob\b)|(heap.)?(out(side)?.of.bound(s)?|\boob\b)(?!.(read|write))',
        # resource
        'uninitialized':r'uninitialized',
        'validation':r'((incomplete|incorrect|lack.of|invalid|missing).)?\bvalidat(e|ion)(d|s)?\b(?!.(dataset|set|data|loss|accuracy|result|gradient|step|error))',
        # other
        'denial of service':r'denial.of.service|\bdos\b',
        'type confusion':r'type.confusion',
        'core dump':r'core.dump',
        'crash':r'crash',
        'undefined behavior':r'undefined.behavio(u)?r|misbehave',
        'segmentation fault':r'seg(ment)?(ation)?(.)?fault', # improper memory access
        'arbitrary code execution':r'arbitrary.code.execution',
        'security':r'(in)?secur(e|ity)',
        'deadlock':r'dead(.)?lock',
        'check fail':r'check.(.)?fail|fail(ing|ed)?(.)?check|assertion.fail',
        'code injection':r'code injection',
        'abort':r'abort',
        'format string':r'format.string|string.format',
        'vuln':r'vuln',
    }

REGEX_ENHENCE = {
    'race condition':r'\brac(e|ing)', # CWE-362
    'improper access control':r'unauthenticated|gain.access|permission', # CWE-284
    'attack':r'attack',
    'threat':r'threat',
    'violate':r'violate',
    'fatal':r'fatal',
    'overrun':r'overrun', 
    'underflow':r'underflow',
    'remote code execution':r'remote.code.execution|\brce\b',
    'cve':r'\bcve\b',
    'cwe':r'\bcwe\b',
    'malicious':r'malicious',
    'poison':r'posion',
    #------------------------------- Not mention by Related Work -----------------------------------
    'overflow': r'overflow(?!.com)?', # avoid stackoverflow.com
    'safety':r'unsafe|thread.safe|safer',
    'dead code':r'dead(.)?code', # CWE-561 
    'shape check':r'shape.check|check.shape', 
}

class VulnerabilityRegex:
    regex = REGEX
    regex_enhence = REGEX_ENHENCE
    
    def __init__(self):
        pass
    
    @staticmethod
    def basic():
        return '|'.join(list(VulnerabilityRegex.regex.values()))

    @staticmethod
    def enhence():
        return '|'.join(list(VulnerabilityRegex.regex_enhence.values()))
    
    @staticmethod
    def normalize_searchkey(df_col):
        col = df_col.copy()
        for key,value in VulnerabilityRegex.regex.items():
            col = col.str.replace(value, key, case=False, regex=True)
        return col

    @staticmethod
    def normalize_enhence_searchkey(df_col):
        col = df_col.copy()
        for key,value in VulnerabilityRegex.regex_enhence.items():
            col = col.str.replace(value, key, case=False, regex=True)
        return col


if __name__ == "__main__":
    print("[INF] Begin.")

    vuleRegex = VulnerabilityRegex()
    print(vuleRegex.all())
    print("[INF] Completed!")