import './MessageGroupFeed.css';
import MessageGroupItem from './MessageGroupItem';

export default function MessageGroupFeed(props) {
  print(props)
  return (
    <div className='message_group_feed'>
      <div className='message_group_feed_heading'>
        <div className='title'>Messages</div>
      </div>
      <div className='message_group_feed_collection'>
        {props.message_groups.map((message_group,a) => {
        return  <MessageGroupItem key={a} message_group={message_group} />
        })}
      </div>
    </div>
  );
}