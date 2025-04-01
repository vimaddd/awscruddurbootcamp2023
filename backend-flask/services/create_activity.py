from datetime import datetime, timedelta, timezone
from lib.db import db

class CreateActivity:
    @staticmethod
    def run(message, user_handle, ttl):
        """
        Aktivite oluşturma işlemini yürütür
        
        Args:
            message (str): Aktivite mesajı
            user_handle (str): Kullanıcı handle'ı
            ttl (str): Aktivite süresi ('30-days', '7-days', vb.)
            
        Returns:
            dict: {'errors': list, 'data': dict}
        """
        model = {
            'errors': [],
            'data': None
        }

        # 1. TTL Validasyonu
        ttl_map = {
            '30-days': timedelta(days=30),
            '7-days': timedelta(days=7),
            '3-days': timedelta(days=3),
            '1-day': timedelta(days=1),
            '12-hours': timedelta(hours=12),
            '3-hours': timedelta(hours=3),
            '1-hour': timedelta(hours=1)
        }
        
        if ttl not in ttl_map:
            model['errors'].append({'code': 'invalid_ttl', 'message': 'Geçersiz TTL değeri'})

        # 2. Kullanıcı Handle Validasyonu
        if not user_handle or not isinstance(user_handle, str):
            model['errors'].append({'code': 'invalid_handle', 'message': 'Geçersiz kullanıcı handle'})

        # 3. Mesaj Validasyonu
        if not message or not isinstance(message, str):
            model['errors'].append({'code': 'invalid_message', 'message': 'Mesaj boş olamaz'})
        elif len(message) > 280:
            model['errors'].append({'code': 'message_too_long', 'message': 'Mesaj 280 karakteri aşamaz'})

        # Hata varsa erken dönüş
        if model['errors']:
            model['data'] = {
                'handle': user_handle,
                'message': message,
                'ttl': ttl
            }
            return model

        try:
            # 4. Aktiviteyi oluştur
            expires_at = datetime.now(timezone.utc) + ttl_map[ttl]
            uuid = CreateActivity._create_activity(user_handle, message, expires_at)
            
            # 5. Oluşturulan aktiviteyi getir
            activity = CreateActivity._get_activity(uuid)
            
            if not activity:
                model['errors'].append({'code': 'activity_not_created', 'message': 'Aktivite oluşturulamadı'})
                return model
                
            model['data'] = activity
            return model

        except Exception as e:
            model['errors'].append({'code': 'database_error', 'message': str(e)})
            return model

    def _create_activity(handle, message, expires_at):
      try:
          sql = """
          INSERT INTO activities (
              user_uuid,
              message,
              expires_at
          ) VALUES (
              (SELECT uuid FROM users WHERE handle = %(handle)s LIMIT 1),
              %(message)s,
              %(expires_at)s
          ) RETURNING uuid;
          """
          print(f"🚀 Çalıştırılan SQL: {sql}")
          
          result = db.query_commit(sql, {
              'handle': handle,
              'message': message,
              'expires_at': expires_at
          })
          
          if not result:
              raise ValueError("Aktivite UUID dönülmedi")
              
          print(f"✅ Aktivite oluşturuldu, UUID: {result}")
          return result
          
      except Exception as e:
          print(f"❌ Aktivite oluşturma hatası: {e}")
          raise

    @staticmethod
    def _get_activity(uuid):
        """Aktivite detaylarını getirir"""
        sql = db.template('activities','object')
        return db.query_object_json(
            sql,
            {'uuid': uuid}
        )

 