from contextlib import contextmanager


@contextmanager
def execute_query(connection, query):
    '''query context manager'''
    cursor = connection.cursor(buffered=True)
    cursor.execute(query)
    connection.commit()
    yield cursor.fetchall()
    cursor.close()


def sanitize(args, constraints):
    valid_args = {}
    for arg in args.keys():
        valid_args[arg] = args[arg]
        if arg in constraints:
            acs = constraints[arg]
            for ac in acs:
                if not ac.check(arg, args[arg]):
                    del valid_args[arg]
                    print("check failed: '" + str(arg) + "' : '" + str(args[arg]) + "'")
                    break
    return valid_args

# Constraints are used to check whether text input is valid


def get_representation(request):
    mimetypes = request.accept_mimetypes

    representation = 'text/json'
    if ('text/json' not in mimetypes) and ('text/csv' in mimetypes):
        representation = 'text/csv'
    return representation


class Constraint():
    def check(self, input):
        pass


class TypeConstraint(Constraint):
    supported_types = ['int', 'str', 'float']

    def __init__(self, type):
        self.type = type
        if self.type not in self.supported_types:
            raise TypeError('Type is not supported.')

    def check(self, name, input):
        '''returns True iff input is a valid instance of the defined type'''
        input = str(input)
        # str
        if(self.type == 'str'):
            for char in input:
                n = ord(char)
                if not ((n >= ord('a') and n <= ord('z'))
                        or (n >= ord('A') and n <= ord('Z'))
                        or (n >= ord('0') and n <= ord('9'))
                        or n == ord(' ')):
                    return False
        if(self.type == 'int'):
            # negative sign
            if(input[0] == '-'):
                input = input[1:]
            for char in input:
                n = ord(char)
                if not (n >= ord('0') and n <= ord('9')):
                    return False
        if(self.type == 'float'):
            # negative sign
            if(input[0] == '-'):
                input = input[1:]
            dot = False
            for char in input:
                n = ord(char)
                if not (n >= ord('0') and n <= ord('9')):
                    if(not dot and n == ord('.')):
                        dot = True
                    else:
                        return False
        return True


class LengthConstraint(Constraint):
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def check(self, name, input):
        '''returns True iff input length is in the range [self.min, self.max]'''
        if len(input) >= self.min and len(input) <= self.max:
            return True
        return False


class ValueConstraint(Constraint):
    def __init__(self, valid_values):
        self.valid_values = valid_values

    def check(self, name, input):
        return input in self.valid_values


class CustomConstraint(Constraint):
    def __init__(self, function):
        self.function = function

    def check(self, name, input):
        return self.function(name, input)
