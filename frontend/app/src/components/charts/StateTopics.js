// Team members (Team 13):
// Yuansan Liu, 1037351
// Karun Varghese Mathew, 1007247
// Junlin Chen, 1065399
// Jingyi Shao, 1049816
// Han Jiang, 1066425

import React from "react";

import { Divider } from "antd";

function StateTopics() {
  return (
    <div style={{display: 'table', height: '320px'}}>
      <h4>Top Twitter topics in each state</h4>
      <div
        className="topic-contianer"
        style={{
          height: '80%',
          overflowY: "scroll",
          textAlign: "left",
        }}
      >
        <p>
          <b>New South Wales</b>
          <br />
          reopen, test, tests positive for, tested, test, virus, amid,
          symptoms, disease, lungs <br />
          hospital, patient, ventilator, icu, symptoms, deaths, positive,
          number, confirmed, county <br />
          dying, die, home, americans, tested, world, china, war, fighting,
          countries
        </p>

        <Divider />
        <p>
          <b>Victoria</b>
          <br />
          reopen, test, home, masks, americans, tested, study, early, risk, important,
          social <br />
          died, family, complications, member, last week, deaths, number,
          increase, yesterday, numbers <br />
          nhttps, virus, world, here's, staysafe, tips, working from home,
          we're, age, situation
        </p>

        <Divider />
        <p>
          <b>Queensland</b>
          <br />
          reopen, test, home, masks, system, issues, order, stay at home, orders,
          governor, rules <br />
          challenges, focus, issues, lack, critical, trump, dies, calls,
          death, handling <br />
          due, aka, 2020, retweet, like, workers, food, employees, amazon,
          delivery
        </p>

        <Divider />
        <p>
          <b>South Australia</b>
          <br />
          reopen, test, home, masks, food, hospital, patient,
          ventilator, icu, symptoms <br />
          state, response, federal, local, state, patients, surge, hospital,
          hospitals, death toll <br />
          w, folks, we're, wondering, era, share, learn, experts, experience,
          survive
        </p>

        <Divider />
        <p>
          <b>South Australia</b>
          <br />
          due, aka, 2020, retweet, like, times, americans, die, flu, died
          <br />
          anxiety, stress, fear, quarantine, nnhttps, stay home, stay safe,
          stayhome, safe, stayathome <br />
          virus, amid, symptoms, disease, lungs, workers, food, employees,
          amazon, delivery
        </p>

        <Divider />
        <p>
          <b>Western Australia</b>
          <br />
          stay home, stay safe, stayhome, safe, stayathome, peak, model,
          california, projections, models <br />
          patients, symptoms, recovered, blood, study, world, china, war,
          fighting, countries <br />
          due, impacts, lives, changed, normal, news, updates, latest,
          message, local
        </p>

        <Divider />
        <p>
          <b>Tasmania and Northern Territory</b>
          <br />
          students, online, learning, student, challenges, questions, dr,
          answers, join, discuss <br />
          part, leadership, global, lead, plan, florida, fears, market,
          threat, demand <br />
          symptoms, tiger, tests positive for, tested, test, number, more
          than, infected, worldwide, million
        </p>
      </div>
    </div>
  );
}

export default StateTopics;
