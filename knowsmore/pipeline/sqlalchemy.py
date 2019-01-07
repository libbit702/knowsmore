class SqlalchemyPipeline(object):
    def process_item(self, item, spider):
        db_string = 'postgres://%s:%s@%s/%s' % (
            settings['DB_USERNAME'], settings['DB_PASSWORD'], settings['DB_HOST'], settings['DB_NAME']
        )
        db = create_engine(db_string)
        Session = sessionmaker(db)
        session = Session()
        if spider.name is 'psn_game':
            return item
