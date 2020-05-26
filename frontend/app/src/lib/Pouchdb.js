import PouchDB from 'pouchdb'

const url = 'http://shibachan:MuchWOWSuchAmAzE@172.26.131.132/'

function get_db(db_name, replace_url) {
  const turl = replace_url ? replace_url : url;
  return new PouchDB(turl + db_name);
}

export default get_db