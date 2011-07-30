def concordion_convert_parameters(*converters):
	def decorator(functor):
		def func_call(self, *args):
			real_args = []
			for i, converter in enumerate(converters):
				real_args.append(converter(args[i]))
			return functor(self, *real_args)
		func_call.real_func_code = functor.func_code
		func_call._real_name = functor.__name__
		return func_call
	return decorator
