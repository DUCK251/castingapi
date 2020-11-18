from models import Actor, Movie, Role

PAGE_SIZE = 10


class Basefilter:
    '''The class implements filter methods to update query and
    get results by query. Subclass overrides get_results method
    to get filtered results.

    Attribute:
        model: sqlalchemy model
        columns: colums of self.model
        data: dictionary({key(string): value(list)}).
              Using the data, update query.
        query: sqlalchemy query initialized by self.model.query

    Method:
        filter: update query contained in value list of self.data
        filter_by_min: update query greater than or equal to min_value
        filter_by_max: update query less than or equal to max_value
        get_page_info: returns page and page_size by self.data
        paginate: returns total number of query results and
                  paginated results by query
        get_results: update query and returns total number of results and
                     paginated results.
    '''
    def __init__(self, model, data):
        self.model = model
        self.columns = [column.key for column in model.__table__.columns]
        self.data = data
        self.query = model.query

    def filter(self):
        for key, value in self.data.items():
            if key in self.columns:
                model_attr = getattr(self.model, key)
                self.query = self.query.filter(model_attr.in_(value))

    def filter_by_min(self, column, key=None):
        '''
        Args:
            column : column name
            key : data key

            if key is min_column, key can be omitted
            ex) column : age, key : min_age
        Returns:
            None
        '''
        key = key or 'min_' + column
        if key in self.data:
            min_value = self.data[key][0]
            model_column = getattr(self.model, column)
            self.query = self.query.filter(model_column >= min_value)

    def filter_by_max(self, column, key=None):
        '''
        Args:
            column : column name
            key : data key

            if key is max_column, key can be omitted
            ex) column : age, key : max_age
        Returns:
            None
        '''
        key = key or 'max_' + column
        if key in self.data:
            max_value = self.data[key][0]
            model_column = getattr(self.model, column)
            self.query = self.query.filter(model_column <= max_value)

    def get_page_info(self):
        if 'page' in self.data:
            page = int(self.data['page'][0])
        else:
            page = 1

        if 'page_size' in self.data:
            page_size = int(self.data['page_size'][0])
        else:
            page_size = PAGE_SIZE
        return page, page_size

    def paginate(self, page=1, page_size=PAGE_SIZE):
        total_count = self.query.count()
        page = page - 1
        ret = self.query.limit(page_size).offset(page * page_size).all()
        return total_count, ret

    def get_results(self):
        self.filter()
        page, page_size = self.get_page_info()
        return self.paginate(page, page_size)


class Actorfilter(Basefilter):
    def __init__(self, data):
        Basefilter.__init__(self, Actor, data)

    def filter_name_by_search_term(self):
        if 'search_term' in self.data:
            search_term = self.data['search_term'][0]
            criterion = self.model.name.ilike(f'%{search_term}%')
            self.query = self.query.filter(criterion)

    def get_results(self):
        self.filter()
        self.filter_name_by_search_term()
        self.filter_by_min('age')
        self.filter_by_max('age')
        self.filter_by_min('height')
        self.filter_by_max('height')
        page, page_size = self.get_page_info()
        return self.paginate(page, page_size)


class Moviefilter(Basefilter):
    def __init__(self, data):
        Basefilter.__init__(self, Movie, data)

    def filter_title_by_search_term(self):
        if 'search_term' in self.data:
            search_term = self.data['search_term'][0]
            criterion = self.model.title.ilike(f'%{search_term}%')
            self.query = self.query.filter(criterion)

    def get_results(self):
        self.filter()
        self.filter_by_min('release_date')
        self.filter_by_max('release_date')
        self.filter_title_by_search_term()
        page, page_size = self.get_page_info()
        return self.paginate(page, page_size)


class Rolefilter(Basefilter):
    def __init__(self, data):
        Basefilter.__init__(self, Role, data)

    def get_results(self):
        self.filter()
        self.filter_by_min('min_age', 'min_age')
        self.filter_by_max('max_age', 'max_age')
        page, page_size = self.get_page_info()
        return self.paginate(page, page_size)
