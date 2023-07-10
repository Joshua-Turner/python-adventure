class Game:
    def __init__(self, character, path, current_step_id=None):
        self.character = character
        self.path = path
        self.current_step_id = current_step_id if isinstance(
            current_step_id, str) else self.get_first_step_id()

    def get_first_step_id(self):
        return self.path['name']+'.'+self.path['action'][0]['name']

    def is_path(self, path):
        return True if isinstance(path, dict) and isinstance(path['action'], list) else False

    def traverse(self, callback, path=None, base_step_id=None):
        path = path if self.is_path(path) else self.path
        step_id = base_step_id if isinstance(
            base_step_id, str) else path['name']
        for step in path['action']:
            current_step_id = step_id + '.' + step['name']
            is_path = self.is_path(step)
            should_continue = callback(step, is_path, current_step_id)
            print('Traversing should continue from: '+current_step_id+' - '+str(should_continue))
            if should_continue == False:
                break

            if is_path:
                self.traverse(callback, step, current_step_id)

    def find(self, step_id):
        _step = None
        _is_path = None

        def matches_pos(step, is_path, _step_id):
            if step_id == _step_id:
                nonlocal _step
                _step = step
                nonlocal _is_path
                _is_path = is_path
                return False

            return True

        self.traverse(matches_pos)
        if _step is None:
            print('Step ID: "'+step_id+'" not found')
            return False
        return {'step': _step, 'is_path': _is_path}

    def play(self, from_path=None):
        new_step_id = from_path if isinstance(
            from_path, str) else self.current_step_id
        step = self.find(new_step_id)

        if step == False:
            return

        self.current_step_id = new_step_id
        running = False

        def run_step(step, is_path, step_id):
            if step_id == self.current_step_id:
                nonlocal running
                running = True

            if not running:
                return True

            if not is_path:
                result = step['action'](
                    character=self.character, step_id=step_id)
                if result != True:
                    if isinstance(result, str):
                        self.play(result)
                    return False

            return True

        self.traverse(run_step)