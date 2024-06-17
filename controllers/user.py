from flask import jsonify, request
from datetime import datetime
from models.client import Client , FI, CP, MP, CP_PRICE, db

def get_clients():
    filters = {}
    for field in ['full_name', 'client_id', 'id_number']:
        value = request.args.get(field)
        if value:
            filters[field] = value

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        clients = Client.query.filter(Client.ac_open_date.between(start_date, end_date)).all()
    else:
        clients = Client.query.filter_by(**filters).all()

    client_data = [{'full_name': client.full_name,
                    'client_id': client.client_id,
                    'ac_open_date': str(client.ac_open_date),
                    'id_number': client.id_number,
                    'birthday': str(client.birthday)
                    } for client in clients]
    return jsonify(client_data)



def get_client_total_instrument_value(client_id):
    query = db.session.query(
        CP.client_id,
        db.func.sum(CP.drawable_qty * CP_PRICE.closing_price).label('total_value')
    ).join(
        CP_PRICE,
        CP_PRICE.instrument_id == CP.instrument_id
    ).filter(
        CP.client_id == client_id
    ).group_by(
        CP.client_id
    )

    result = query.first()

    if result:
        return result.total_value
    else:
        return 0


def get_client_property(client_id):
    client_id = request.view_args.get('client_id')
    
    fi_count = db.session.query(db.func.sum(FI.amount)).filter(FI.tkck == '048' + client_id).scalar()
    print("fi: " ,fi_count)
    
    mp_count = db.session.query(db.func.sum(MP.amount)).filter(MP.tkck == '048' + client_id).scalar()
    print("mp: ", mp_count)
    
    cp_count = get_client_total_instrument_value(client_id)
    print("cp: ", cp_count)
    return jsonify({'fi_count': fi_count, 'cp_count': cp_count, 'mp_count': mp_count})
