package spring.entities;

import java.time.Duration;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name="users")
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "email")
    public String email;
    
    @Column(name = "nicknames", nullable = false)
    public List<Float> nicknames = new ArrayList<>(Arrays.asList(1.2f, 3.2f));
    
    @Column(name = "age", nullable = false)
    public Integer age = 2;
    
    @Column(name = "birthday", nullable = false)
    protected Duration birthday;
    
    @Column(name = "first_name")
    public String firstName = "John";
    
    public User() { }

    public User(String email, List<Float> nicknames, Integer age, Duration birthday, String firstName) {
        this.email = email;
        this.nicknames = nicknames;
        this.age = age;
        this.birthday = birthday;
        this.firstName = firstName;
    }
    
    public String getEmail() {
        return this.email;
    }

    public void setEmail(String email) {
        this.email = email;
    }
    
    public List<Float> getNicknames() {
        return this.nicknames;
    }

    public void setNicknames(List<Float> nicknames) {
        this.nicknames = nicknames;
    }
    
    public Integer getAge() {
        return this.age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }
    
    public Duration getBirthday() {
        return this.birthday;
    }

    public void setBirthday(Duration birthday) {
        this.birthday = birthday;
    }
    
    public String getFirstname() {
        return this.firstName;
    }

    public void setFirstname(String firstName) {
        this.firstName = firstName;
    }
    
}